<div align="center">

# 📚 LivroAI

### Encontre livros a partir de uma foto da estante

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-05998b)

</div>

---

## 💡 Sobre o projeto

O **LivroAI** processa uma imagem da estante e retorna:

- livros detectados/enriquecidos
- recomendações de leitura por sessão

Atualmente o fluxo usa segmentação por YOLO em um Space do Hugging Face, OCR no Google Vision e pós-processamento com LLM.

---

## ✨ Funcionalidades atuais

- 📸 Upload de imagem via endpoint de análise
- 🧩 Segmentação de objetos com YOLO (HF Space externo)
- 🔎 OCR por recorte (bbox) com Google Vision API
- 🧠 Limpeza de títulos e geração de recomendações com Mistral
- 📚 Enriquecimento via Google Books API
- 💾 Persistência em Supabase (PostgreSQL + Storage)
- ⏱️ Sessões temporárias com expiração

---

## 🧱 Stack

| Camada | Tecnologia |
|---|---|
| Backend | FastAPI + SQLAlchemy async |
| Banco/Storage | Supabase (PostgreSQL + Storage) |
| Detecção | YOLO via Hugging Face Space |
| OCR | Google Cloud Vision |
| IA textual | Mistral API |
| Frontend | React + Vite |
| Local dev | Docker Compose |

---

## 🔄 Fluxo de análise

```
Foto da estante
  -> YOLO (HF Space) retorna bboxes
  -> recorte das bboxes
  -> OCR Google Vision em cada recorte
  -> limpeza dos títulos (Mistral)
  -> busca/enriquecimento (Google Books)
  -> recomendações (Mistral)
  -> persistência em sessoes/analise_yolo/recomendacoes
```

Observação: nomes não encontrados no Google Books são ignorados sem derrubar o fluxo.

---

## 🗄️ Modelo de dados

```
livros ◄──── recomendacoes ────► sessoes
                                    │
                                    └──── analise_yolo
```

| Tabela | Descrição |
|---|---|
| `livros` | Catálogo de livros enriquecidos |
| `sessoes` | Sessões de análise com expiração |
| `recomendacoes` | Recomendações geradas por sessão |
| `analise_yolo` | Foto, bboxes e entradas usadas na análise |

---

## 🔌 Endpoints principais

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/v1/analise/` | Envia foto e retorna livros + recomendações |
| `GET` | `/api/v1/sessoes/{id}` | Busca resultado da sessão |
| `GET` | `/api/v1/sessoes/{id}/valida` | Verifica se sessão está ativa |
| `DELETE` | `/api/v1/sessoes/{id}` | Remove sessão |
| `GET` | `/api/v1/livros` | Lista catálogo de livros |
| `GET` | `/api/v1/livros/{isbn}` | Busca livro por ISBN/UUID |
| `POST` | `/api/v1/livros` | Adiciona livro via Google Books |
| `GET` | `/health` | Health check da API |

---

## ⚙️ Variáveis de ambiente

### Obrigatórias

```
DATABASE_URL
SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_SERVICE_KEY
HF_SPACE_URL
HF_TOKEN
GOOGLE_BOOKS_API_KEY
```

### Opcionais

```
STORAGE_BUCKET=Pratileiras
STORAGE_BUCKET_FOTOS=Pratileiras
MISTRAL_API_KEY=
GOOGLE_VISION_API_KEY=
APP_ENV=development
APP_NAME=LivroAI
API_PREFIX=/api/v1
DEBUG=true
PORT=8000
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
YOLO_CONFIDENCE_THRESHOLD=0.6
```

## 🐳 Execução local (Docker)

### Pré-requisitos

- Docker Desktop ativo
- arquivo `.env` na raiz
- credencial GCP em `app/cred/` (se OCR estiver habilitado)

### Subir backend + frontend

```bash
docker compose up --build
```

### URLs

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs` (quando `DEBUG=true`)
- Frontend: `http://localhost:5173`

### Comandos úteis

```bash
docker compose up -d
docker compose logs -f backend
docker compose down
```

---

## 🧪 Teste rápido da análise

No PowerShell 5.1 (sem `-Form`):

```powershell
$img = "$env:USERPROFILE\Downloads\aaaa.jpg"
curl.exe -X POST "http://localhost:8000/api/v1/analise/" -F "foto=@$img"
```

---

## 📁 Estrutura resumida

```
LivroAI/
├── app/
│   ├── core/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── services/
├── frontend/
├── docker-compose.yml
├── Dockerfile.backend
└── requirements.txt
```
