import json
import os
import cv2
import numpy as np
from PIL import Image

# ===== Config =====
INPUT = "capa_original.png"
OUTPUT_IMG = "capa_folha_anotada.png"
OUTPUT_JSON = "capa_folha_areas.json"

ALPHA = 0.47
GRID = False
GRID_STEP = 100
DOBRA_AUTO = True
DOBRA_Y = None
CABECALHO_BLOQUEADO = True
ALTURA_CABECALHO = 130
# ===================

COLORS = {
    1: (255, 0, 0),       # azul
    2: (0, 200, 0),       # verde
    3: (100, 0, 200),     # rosa escuro
    4: (193, 182, 255),   # rosa claro
}

LEVEL_NAMES = {
    1: "nível 1 (azul)",
    2: "nível 2 (verde)",
    3: "nível 3 (rosa escuro)",
    4: "nível 4 (rosa claro)"
}


def alpha_rect(img, pt1, pt2, color_bgr, alpha):
    x1, y1 = pt1
    x2, y2 = pt2
    x1, x2 = sorted([max(0, x1), min(img.shape[1]-1, x2)])
    y1, y2 = sorted([max(0, y1), min(img.shape[0]-1, y2)])
    if x2 <= x1 or y2 <= y1:
        return img
    overlay = img.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), color_bgr, thickness=-1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    return img   # <<< borda preta removida


def draw_grid(img):
    if not GRID:
        return
    h, w = img.shape[:2]
    for x in range(0, w, GRID_STEP):
        cv2.line(img, (x, 0), (x, h), (0,0,0), 1)
        cv2.putText(img, str(x), (x+3, 14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1, cv2.LINE_AA)
    for y in range(0, h, GRID_STEP):
        cv2.line(img, (0, y), (w, y), (0,0,0), 1)
        cv2.putText(img, str(y), (3, y+14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1, cv2.LINE_AA)


def draw_dobra(img, y=None):
    h, w = img.shape[:2]
    y = (h // 2) if DOBRA_AUTO or y is None else int(y)
    for x in range(0, w, 20):
        cv2.line(img, (x, y), (min(x+10, w-1), y), (0,0,0), 2)


def render(base_bgr, boxes, dobra_y):
    canvas = base_bgr.copy()
    if CABECALHO_BLOQUEADO:
        head = base_bgr[:ALTURA_CABECALHO, :].copy()

    for b in boxes:
        color = COLORS[b["level"]]
        alpha_rect(canvas, (b["x1"], b["y1"]), (b["x2"], b["y2"]), color, ALPHA)

    if CABECALHO_BLOQUEADO:
        canvas[:ALTURA_CABECALHO, :] = head

    draw_dobra(canvas, dobra_y)
    draw_grid(canvas)
    return canvas


def save_outputs(base_bgr, boxes, dobra_y):
    img = render(base_bgr, boxes, dobra_y)
    cv2.imwrite(OUTPUT_IMG, img)
    data = {
        "dobra_y": (base_bgr.shape[0] // 2) if DOBRA_AUTO else (int(dobra_y) if dobra_y is not None else None),
        "boxes": boxes
    }
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Salvo: {OUTPUT_IMG}  e  {OUTPUT_JSON}")


def main():
    if not os.path.exists(INPUT):
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT}")

    pil = Image.open(INPUT).convert("RGB")
    base_bgr = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    h, w = base_bgr.shape[:2]
    dobra_y = (h // 2) if DOBRA_AUTO else (DOBRA_Y if DOBRA_Y is not None else (h // 2))

    boxes = []
    current_level = 1
    pts = []

    window = "Anotação de Capa (OpenCV)"
    cv2.namedWindow(window, cv2.WINDOW_AUTOSIZE)

    def mouse_cb(event, x, y, flags, param):
        nonlocal pts, boxes, current_level
        if event == cv2.EVENT_LBUTTONDOWN:
            if CABECALHO_BLOQUEADO and y < ALTURA_CABECALHO:
                print("⚠️ Cabeçalho bloqueado — selecione abaixo.")
                return
            pts.append((x, y))
            if len(pts) == 2:
                (x1, y1), (x2, y2) = pts
                x1, x2 = sorted([x1, x2])
                y1, y2 = sorted([y1, y2])
                if x2 > x1 and y2 > y1:
                    boxes.append({
                        "level": current_level,
                        "x1": int(x1), "y1": int(y1),
                        "x2": int(x2), "y2": int(y2)
                    })
                pts = []

    cv2.setMouseCallback(window, mouse_cb)

    while True:
        canvas = render(base_bgr, boxes, dobra_y)
        hud = f"Nível atual: {LEVEL_NAMES[current_level]} | Caixas: {len(boxes)}"
        cv2.rectangle(canvas, (0,0), (canvas.shape[1], 28), (255,255,255), -1)
        cv2.putText(canvas, hud, (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,0), 1, cv2.LINE_AA)

        cv2.imshow(window, canvas)
        key = cv2.waitKey(20) & 0xFF

        if key in [ord('1'), ord('2'), ord('3'), ord('4')]:
            current_level = int(chr(key))
            print(f"→ Nível alterado para {LEVEL_NAMES[current_level]}")
        elif key == ord('u'):
            if boxes: boxes.pop()
        elif key == ord('s'):
            save_outputs(base_bgr, boxes, dobra_y)
        elif key == ord('q') or key == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
