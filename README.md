# Anotação de Capas de Jornais

Este repositório contém um script em **Python + OpenCV** para anotar capas de jornais com retículas coloridas que indicam a hierarquia de importância das chamadas jornalísticas.

---

## 🎯 Objetivo
Facilitar a análise de enquadramento jornalístico mostrando visualmente:
- **Nível 1 (azul)** → manchete principal
- **Nível 2 (verde)** → chamadas secundárias
- **Nível 3 (rosa escuro)** → chamadas de menor destaque
- **Nível 4 (rosa claro)** → chamadas na metade inferior da capa (após a dobra do jornal)

---

## ⚙️ Requisitos

Instalar dependências:

```bash
pip install opencv-python pillow

## ▶️ Uso

Coloque a capa que deseja anotar na pasta do projeto com o nome:


Execute o script:

```bash
python anotar_capa_interativo.py


Vai aparecer formatado bonitinho no GitHub como instruções para o usuário:

---

## ▶️ Uso

Coloque a capa que deseja anotar na pasta do projeto com o nome:

Controles para a anotação
Na janela que abre, pode-se ver os controles no topo. 
Os números selecionam os níveis de destaque. 
Para alterar o nível em uso clique na área dos comandos e depois clique no teclado o número do nível.

1, 2, 3, 4 → selecionar nível de destaque

Para criar a marcação na página:

Clique 1 + Clique 2 → marcar canto superior esquerdo e inferior direito da chamada

Comandos importantes:
u → desfaz última marcação

s → salva resultado (capa_folha_anotada.png + capa_folha_areas.json)

g → liga/desliga grid de coordenadas

q ou Esc → sair

📂 Saídas geradas

capa_folha_anotada.png → capa anotada com retículas coloridas

capa_folha_areas.json → arquivo JSON com as coordenadas

📖 Observação

Este projeto faz parte de um trabalho acadêmico de doutoramento em Comunicação (UBI).


---
