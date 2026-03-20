<div align="center">

# 📚 LivroAI

**Descubra novos livros analisando sua estante com IA** ✨

[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009485?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ed?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/status-em%20produção-green?style=flat-square)](https://livroai.vercel.app)

[🌐 Demo ao vivo](https://livroai.vercel.app) • [📖 Documentação](#-guia-de-uso) • [🤝 Contribuir](#-contribuindo)

</div>

---

## 🎯 Resumo

**LivroAI** é uma plataforma que combina **visão computacional** e **inteligência artificial** para analisar fotos de estantes de livros e:

- 📷 **Detectar automaticamente** todos os livros na imagem
- 📚 **Enriquecer dados** com informações do Google Books
- 🤖 **Gerar recomendações personalizadas** com base no perfil de leitura
- 💾 **Manter histórico** de análises com sessões seguras

## ✨ Funcionalidades

### Core
- ✅ Upload de imagem com análise em tempo real (~30-60s)
- ✅ Detecção de livros com **YOLO** (via Hugging Face Space)
- ✅ OCR automático com **Google Cloud Vision**
- ✅ Limpeza de títulos e recomendações com **Mistral LLM**
- ✅ Enriquecimento com metadata via **Google Books API**
- ✅ Histórico de sessões com expirações (24h)

### Segurança
- 🔐 Autenticação de sessão com **tokens únicos por análise**
- 🛡️ CORS configurado para produção
- 🚀 Proteção contra acesso não autorizado a sessões alheias

### UX
- 🎨 Interface luxury design com animações suaves
- 🎯 Progresso visual em 5 etapas durante análise
- 📱 Totalmente responsivo (mobile-first)
- 🔍 Filtros no catálogo (detectados / recomendados)

---

## 🧱 Tech Stack

| Camada | Tech | Justificativa |
|---|---|---|
| **Backend** | FastAPI + SQLAlchemy async | Performance, type-safety, async I/O |
| **Database** | Supabase (PostgreSQL) | Full-stack SQL, real-time ready |
| **Storage** | Supabase Storage | Integrado com o banco, CDN |
| **Detecção** | YOLO (HF Space) | Precisão + serverless |
| **OCR** | Google Cloud Vision | Robustez em lombadas inglesas/tortas |
| **IA** | Mistral API | Custo-benefício, regra europeia |
| **Frontend** | React 18 + Vite | Fast HMR, bundling otimizado |
| **State** | Zustand | Simplicidade vs Redux |
| **Styling** | CSS Modules + Variables | Componentização, temas |
| **HTTP** | Axios | Interceptors para request IDs |
| **Deploy** | Vercel | Python runtime, scaling automático |

---

## 📁 Estrutura do Projeto

```
LivroAI/
├── app/                          # Backend FastAPI
│   ├── core/
│   │   ├── config.py            # Settings com Pydantic
│   │   ├── database.py          # SQLAlchemy async setup
│   │   └── main.py              # FastAPI app + middleware
│   ├── models/                  # SQLAlchemy ORM
│   │   ├── sessao.py            # Sessões com token
│   │   ├── livro.py             # Catálogo de livros
│   │   ├── recomendacao.py      # Recomendações geradas
│   │   └── analise_yolo.py      # Metadados de análise
│   ├── routers/                 # Endpoints FastAPI
│   │   ├── analise.py           # POST /analise/
│   │   ├── sessoes.py           # GET/DELETE /sessoes/
│   │   └── livros.py            # GET/POST /livros/
│   ├── schemas/                 # Pydantic request/response
│   │   ├── sessao.py
│   │   ├── livro.py
│   │   └── recomendacao.py
│   └── services/                # Lógica de negócio
│       ├── analise_service.py   # Orquestração pipeline
│       ├── yolo_service.py      # Chamadas ao HF Space
│       ├── ocr_service.py       # Google Vision wrapper
│       ├── ia_service.py        # Mistral LLM wrapper
│       ├── livro_service.py     # Google Books + cache
│       └── storage_service.py   # Upload para Supabase
│
├── frontend/                     # React + Vite
│   ├── src/
│   │   ├── components/          # Componentes reutilizáveis
│   │   │   ├── Navbar.jsx       # Navegação fixa
│   │   │   ├── UploadFoto.jsx   # Drag-drop upload
│   │   │   ├── LivrosDetectados.jsx
│   │   │   └── RecomendacaoCard.jsx
│   │   ├── pages/               # Páginas (rotas)
│   │   │   ├── Home.jsx         # Hero + análise
│   │   │   ├── Historico.jsx    # Sessões salvas
│   │   │   └── Catalogo.jsx     # Visão de biblioteca
│   │   ├── services/
│   │   │   ├── api.js           # Axios + interceptors
│   │   │   └── sessao.js        # LocalStorage helper
│   │   ├── store/
│   │   │   └── resultadoStore.js # Zustand global state
│   │   ├── styles/
│   │   │   └── globals.css      # CSS variables + base styles
│   │   ├── App.jsx              # Root component
│   │   └── main.jsx             # Vite entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml           # Backend + frontend (dev)
├── Dockerfile.backend           # Python app
├── Dockerfile.frontend          # Node build
├── vercel.json                  # Config Vercel
├── requirements.txt             # Python deps
├── .env.example                 # Template env
└── README.md                    # Este arquivo
```

---

## 🚀 Quick Start

### Pré-requisitos

- **Docker Desktop** (recomendado)
- ou **Python 3.11+** + **Node.js 18+** (local)
- arquivo `.env` (veja `.env.example`)

### Setup local com Docker

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/LivroAI.git
cd LivroAI

# Copie o template de ambiente
cp .env.example .env

# Edite .env com suas credenciais (veja ⚙️ abaixo)
# IMPORTANTE: Obtenha as chaves antes de rodar!

# Suba backend + frontend
docker compose up --build

# Em outro terminal, aplique migrations (se necessário)
docker compose exec backend python -m alembic upgrade head
```

**URLs**
- 🌐 Frontend: http://localhost:5173
- 🔧 API: http://localhost:8000
- 📖 Swagger Docs: http://localhost:8000/docs (DEBUG=true)

### Setup local sem Docker

```bash
# Backend
cd LivroAI
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)
python -m uvicorn app.core.main:app --reload

# Frontend (em outro terminal)
cd frontend
npm install
npm run dev
```

---

## ⚙️ Configuração (Environment Variables)

Copie `.env.example` → `.env` e preencha:

### Obrigatórias (`DATABASE_URL`, `SUPABASE_*`, etc)

```bash
# Supabase (https://supabase.com)
DATABASE_URL=postgresql://user:pass@host:5432/db
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_KEY=eyJxxx...

# Hugging Face (para YOLO Space)
HF_SPACE_URL=https://huggingface.co/spaces/seu-user/seu-space/api
HF_TOKEN=hf_xxx

# Google (Vision + Books)
GOOGLE_VISION_API_KEY=AIzaSyxxx
GOOGLE_BOOKS_API_KEY=AIzaSyxxx

# Mistral (LLM)
MISTRAL_API_KEY=xxxxxxxxxxx
```

### Opcionais

```bash
# App
APP_ENV=production              # development | production
DEBUG=false                     # Desabilita /docs em prod
PORT=8000
YOLO_CONFIDENCE_THRESHOLD=0.6

# Frontend
VITE_API_URL=https://api.seu-dominio.com

# CORS
ALLOWED_ORIGINS=https://seu-dominio.com,https://www.seu-dominio.com
ALLOWED_ORIGIN_REGEX=^https://([a-zA-Z0-9-]+\.)*vercel\.app$
```

---

## 🔄 Fluxo de Análise

```mermaid
graph TD
    A[Foto da Estante] -->|upload| B[FastAPI]
    B -->|POST /analise/| C[Gera Session + Token]
    C -->|salva em DB| D[YOLO Detection]
    D -->|bboxes → HF Space| E{Livros encontrados?}
    E -->|SIM| F[Google Vision OCR]
    E -->|NÃO| Z1[Erro: Sem livros]
    F -->|textos| G[Mistral Cleanup]
    G -->|títulos limpos| H[Google Books Enrichment]
    H -->|metadata| I[Mistral Recommendations]
    I -->|justificativas| J[Salva em DB]
    J -->|SessaoResultado| K[Frontend]
    K -->|localStorage| L[Histórico Local]
    L -->|token em header| M[Recupera sessão]
```

**Duração esperada**: 30-60s (incluindo IO externo)

---

## 🔐 Segurança

### Proteção de Sessão

- Cada análise gera um **token único** (`secrets.token_hex(32)`)
- Token é retornado na resposta e salvo em `localStorage`
- Endpoint `/sessoes/{id}` exige header `x-session-token`
- Sem token válido → **403 Forbidden**
- Sessões expiram em **24 horas**

### CORS

- Frontend + Backend no mesmo domínio (Vercel)
- Regex permite subdomínios de preview (CI/CD)
- Localhost habilitado em `DEBUG=true`

### Logging

- Cada request tem `x-client-request-id` para correlação
- Logs incluem duração por etapa (YOLO, OCR, IA)
- Vercel fornece `x-vercel-id` para debugging

---

## 📊 Endpoints

### Análise
```http
POST /api/v1/analise/
Content-Type: multipart/form-data

foto: <arquivo jpg/png>

Response:
{
  "sessao_id": "uuid",
  "token": "token_hex_64_chars",
  "livros_detectados": [...],
  "recomendacoes": [...]
}
```

### Sessões
```http
GET  /api/v1/sessoes/{sessao_id}
     Header: x-session-token: <token>

GET  /api/v1/sessoes/{sessao_id}/valida
DELETE /api/v1/sessoes/{sessao_id}
```

### Catálogo
```http
GET /api/v1/livros
GET /api/v1/livros/{isbn_ou_uuid}
POST /api/v1/livros
```

### Health
```http
GET /health
```

---

## 🐛 Troubleshooting

### 504 Gateway Timeout (Vercel)

- ✅ **Aumentou timeout**: `maxDuration: 300` em `vercel.json`
- ✅ **Limitou processamento**: Max 8 livros para enrichment, 6 para recomendações
- ✅ **Batch flush**: Uma única operação DB vs múltiplas
- ✅ **Monitoramento**: Logs mostram duração de cada etapa

Se ainda tiver timeout:
1. Reduz tamanho/qualidade da imagem
2. Verifica plano Vercel (Pro permite maxDuration 900s)
3. Consulta logs com `x-request-id` fornecido no erro

### 400 CORS Preflight

- ✅ **Middleware order**: CORS executa PRIMEIRO (não depois de logging)
- ✅ **Regex pattern**: Aceita `*.vercel.app` + `localhost:port`

### Blank page Frontend

- [ ] Verifica se `VITE_API_URL` está correto
- [ ] Abre DevTools → Network → verifica requests a `/api/v1/...`
- [ ] Testa health: `curl https://seu-api.vercel.app/health`

---

## 🚀 Deployment

### Vercel (Recomendado)

1. **Conecte seu repositório** no Vercel
2. **Configure environment variables** no projeto
3. **Deploy automático** em cada `git push main`

```bash
# Ou manual
vercel --prod
```

### Alternativas

- **Railway**: Suporta Docker + PostgreSQL
- **Render**: Similar ao Railway
- **DigitalOcean App Platform**: Mais controle

---

## 🤝 Contribuindo

Quer melhorar o LivroAI? Abra uma **issue** ou **pull request**!

```bash
# Clone seu fork
git clone https://github.com/seu-usuario/LivroAI.git
git checkout -b feature/sua-feature

# Faça as mudanças, commit e push
git push origin feature/sua-feature

# Abra PR contra main
```

**Áreas com oportunidades:**
- [ ] Suporte a múltiplos idiomas
- [ ] Dashboard de analytics
- [ ] Export para Goodreads/Skoob
- [ ] Modo offline com cache

---

## 📝 Licença

Este projeto é licenciado sob a **MIT License** - veja [LICENSE](LICENSE) para detalhes.

---

## 👤 Autor

Desenvolvido por [Jairo](https://github.com/seu-usuario)

- 🐙 GitHub: [@seu-usuario](https://github.com/seu-usuario)
- 💼 LinkedIn: [/in/seus-detalhes](https://linkedin.com/in/)

---

## 🙏 Agradecimentos

- **Hugging Face** pelos YOLOv8 Spaces públicos
- **Google** por Vision API e Books API
- **Supabase** pelo PostgreSQL gerenciado
- **Mistral** pela IA aberta
- **Vercel** pelo hosting serverless

---

<div align="center">

**⭐ Se curtiu, deixa uma star! ⭐**

Feito com ❤️ in 🇧🇷

</div>
