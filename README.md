# Brazilian Math YouTube Channels
Este repositório contém os dados coletados por meio da API YouTube Data v3,
referentes ao artigo científico
“Análise de Canais de YouTube Brasileiros Dedicados ao Ensino de Matemática”.

## Fonte dos dados
Os dados foram obtidos a partir da API YouTube Data v3 e referem-se a canais
brasileiros dedicados ao ensino de matemática, com no mínimo 10 mil inscritos.

## Critérios de inclusão
- Canal com conteúdo majoritariamente voltado ao ensino de matemática
- Canal brasileiro
- Mínimo de 10.000 inscritos no momento da coleta

## Data da coleta
Os dados foram coletados em: 2026-01-12.

## Estrutura do repositório
data/└ raw/
      
      ├ dados_canais_youtube.csv
      ├ all_videos.csv
      ├ video_details.csv

scripts/
      
      ├ extrair_ids_canais.py
      ├ analise_canais_youtube.py

## Funcionalidades dos Scripts

### Extração de IDs
Script para converter URLs/handles de canais YouTube em IDs oficiais (UC...)

---

### Coleta de dados via API
- Estatísticas dos canais
- Estatísticas dos vídeos
- Duração dos vídeos
- Curtidas, comentários e visualizações

---

### Processamento e análise
- Cálculo do Índice de Performance
- Estatísticas descritivas
- Boxplots e correlações
- Ranking de canais

---

### Análise de vídeos (Top vídeos por canal)
Permite filtrar por:

- Índice de performance mínimo
- Ano específico
- Métrica (Curtidas, Comentários, Visualizações)

---

## ▶️ Como executar

### 1️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar API Key (Opcional)
Caso queira coletar novos dados:
```
api_key = "SUA_CHAVE"
requisitar_da_api = True
```
Caso contrário:

```
requisitar_da_api = False
```
---

### 3️⃣ Executar script principal
python analise_canais_youtube.py

---

## Observações
Os arquivos CSV permitem reprodutibilidade sem necessidade de acesso à API.

---

## Licença
Uso acadêmico e educacional.
