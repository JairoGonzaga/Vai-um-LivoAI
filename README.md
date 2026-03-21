<div align="center">

# 📚 LivroAI

**Descubra livros analisando sua estante com IA** ✨

![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009485?style=flat-square)
![React](https://img.shields.io/badge/React-18+-61dafb?style=flat-square)
![Status](https://img.shields.io/badge/status-em%20produção-green?style=flat-square)

[🌐 Demo](https://livroai.vercel.app) • [📖 Docs](#-documentação) • [🤝 Contribuir](#-contributing)

</div>

---

## 💡 O que é?

**LivroAI** processa uma foto da sua estante e retorna:

- 📖 **Livros detectados** e enriquecidos com metadata
- 🤖 **Recomendações personalizadas** baseadas no seu perfil de leitura
- 💾 **Histórico de sessões** com acesso seguro via token

O fluxo combina **visão computacional** (YOLO), **OCR** (Google Vision), **LLM** (Mistral) e **enrichment** (Google Books).

---

## ✨ Funcionalidades

- 📸 Upload de imagem com análise em ~30-60s
- 🧩 Detecção automática com YOLO (HF Space)
- 🔎 OCR em lombadas com Google Cloud Vision
- 🧠 Limpeza de títulos + recomendações com Mistral
- 📚 Enriquecimento via Google Books API
- 💾 Persistência em Supabase (PostgreSQL + Storage)
- ⏱️ Sessões temporárias com token (24h)
- 🔐 Acesso seguro (apenas com token correto)
- 🎨 Interface luxury design (mobile-first)

---

## 🧱 Tech Stack

| Camada | Tecnologia |
|---|---|
| Backend | FastAPI + SQLAlchemy async |
| Database | Supabase (PostgreSQL) |
| Storage | Supabase Storage |
| Detecção | YOLO (Hugging Face Space) |
| OCR | Google Cloud Vision |
| IA | Mistral API |
| Frontend | React 18 + Vite |
| Deploy | Vercel (Python + React) |

---

## 🚀 Quick Start

### Com Docker (recomendado)

```bash
git clone https://github.com/seu-usuario/LivroAI.git
cd LivroAI

cp .env.example .env
# Edite .env com suas credenciais

docker compose up --build
```

- 🌐 Frontend: `http://localhost:5173`
- 🔧 API: `http://localhost:8000`
- 📖 Swagger: `http://localhost:8000/docs`

### Sem Docker (Python 3.11+ + Node 18+)

```bash
# Backend
pip install -r requirements.txt
python -m uvicorn app.core.main:app --reload

# Frontend (outro terminal)
cd frontend && npm install && npm run dev
```

---

## 🔄 Fluxo de análise

```
🖼️ Foto da estante
  → YOLO detecta bboxes
  → Google Vision: OCR em cada bbox
  → Mistral: limpa títulos + gera recomendações
  → Google Books: enriquece metadata
  → Supabase: salva resultado
  → 📊 Resultado com token de acesso
```

**Tempo estimado:** 30-60s (incluindo I/O externo)

---

## 🗄️ Banco de Dados

```
Tabelas:
├── livros              (catálogo enriquecido)
├── sessoes             (análises com token + expiração)
├── recomendacoes       (sugestões por sessão)
└── analise_yolo        (metadados: foto, bboxes, textos OCR)
```

---

## 🔌 Endpoints principais

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/v1/analise/` | Envia foto, retorna resultado + token |
| `GET` | `/api/v1/sessoes/{id}` | Busca resultado (requer token no header) |
| `DELETE` | `/api/v1/sessoes/{id}` | Remove sessão |
| `GET` | `/api/v1/livros` | Lista catálogo |
| `GET` | `/health` | Health check |

**Autenticação:** Header `x-session-token: <token>` obrigatório em sessões.

---

## ⚙️ Environment Variables

### Obrigatórias

```bash
# Supabase
DATABASE_URL=postgresql://user:pass@host/db
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...

# Hugging Face (YOLO)
HF_SPACE_URL=https://huggingface.co/spaces/seu/space/api
HF_TOKEN=hf_xxx

# Google APIs
GOOGLE_VISION_API_KEY=AIzaSyxxx
GOOGLE_BOOKS_API_KEY=AIzaSyxxx

# Mistral
MISTRAL_API_KEY=xxx
```

### Opcionais

```bash
APP_ENV=production
DEBUG=false
PORT=8000
ALLOWED_ORIGINS=https://seu-dominio.com
ALLOWED_ORIGIN_REGEX=^https://([a-zA-Z0-9-]+\.)*vercel\.app$
YOLO_CONFIDENCE_THRESHOLD=0.6
API_KEY=sua_api_key_backend
SESSION_TOKEN_SECRET=um_segredo_longo_e_aleatorio
```

### Frontend (Vite)

```bash
VITE_API_URL=https://seu-backend.com/api/v1
VITE_API_BASE_PATH=/api/v1
VITE_API_KEY=sua_api_key_frontend
VITE_AUTH_STORAGE_KEY=livroai_auth_token
```

- `VITE_API_URL`: endpoint base da API (evita URL hardcoded no código).
- `VITE_API_KEY`: enviada como header `x-api-key` em todas as requisições.
- `VITE_AUTH_STORAGE_KEY`: chave usada para ler token de sessão/JWT do `sessionStorage` e enviar como `Authorization: Bearer ...`.
- `SESSION_TOKEN_SECRET`: segredo usado para assinar/validar JWT de sessão (`HS256`) no backend.

Veja `.env.example` para template completo.

---

## 🐳 Docker Compose

```bash
# Subir tudo
docker compose up --build

# Logs
docker compose logs -f backend
docker compose logs -f frontend

# Parar
docker compose down
```

---

## 📁 Estrutura do Projeto

```
LivroAI/
├── app/                          # Backend FastAPI
│   ├── core/
│   │   ├── config.py            # Pydantic settings
│   │   ├── database.py          # SQLAlchemy async
│   │   └── main.py              # FastAPI app
│   ├── models/                  # ORM
│   │   ├── sessao.py            # Com token
│   │   ├── livro.py
│   │   ├── recomendacao.py
│   │   └── analise_yolo.py
│   ├── routers/                 # Endpoints
│   │   ├── analise.py           # POST /analise/
│   │   ├── sessoes.py           # GET/DELETE /sessoes/
│   │   └── livros.py            # GET/POST /livros/
│   ├── schemas/                 # Pydantic
│   │   ├── sessao.py
│   │   ├── livro.py
│   │   └── recomendacao.py
│   └── services/                # Lógica
│       ├── analise_service.py   # Pipeline
│       ├── yolo_service.py
│       ├── ocr_service.py
│       ├── ia_service.py
│       ├── livro_service.py
│       └── storage_service.py
│
├── frontend/                     # React + Vite
│   ├── src/
│   │   ├── components/          # Componentes
│   │   │   ├── Navbar.jsx
│   │   │   ├── UploadFoto.jsx
│   │   │   ├── LivrosDetectados.jsx
│   │   │   └── RecomendacaoCard.jsx
│   │   ├── pages/               # Páginas
│   │   │   ├── Home.jsx         # Análise
│   │   │   ├── Historico.jsx    # Sessões
│   │   │   └── Catalogo.jsx     # Biblioteca
│   │   ├── services/            # API + helpers
│   │   │   ├── api.js           # Axios
│   │   │   └── sessao.js        # SessionStorage
│   │   ├── store/               # Zustand
│   │   │   └── resultadoStore.js
│   │   ├── styles/
│   │   │   ├── globals.css      # CSS vars
│   │   │   └── *.module.css     # Component styles
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml
├── Dockerfile.backend
├── vercel.json                  # Config Vercel
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🧪 Teste rápido

```powershell
# Upload com curl
$img = "$env:USERPROFILE\Downloads\estante.jpg"
curl.exe -X POST "http://localhost:8000/api/v1/analise/" -F "foto=@$img"
```

Resposta inclui:
- `sessao_id`: UUID da análise
- `token`: Token para acessar resultado (keep safe!)
- `livros_detectados`: Array de livros encontrados
- `recomendacoes`: Array de recomendações

---

## 🚨 Troubleshooting

### 504 Gateway Timeout
- ❌ Imagem muito grande → reduz resolução
- ❌ Vercel free tier → atualiza para Pro
- ✅ Verifique logs com `x-request-id` do erro

### 400 CORS Preflight
- ✅ CORS configurado em `app/core/config.py`
- ✅ `ALLOWED_ORIGIN_REGEX` aceita `*.vercel.app`

### Blank page frontend
- ❌ `VITE_API_URL` incorreta?
- ✅ Verifique DevTools → Network

---

## 📝 Licença

MIT License - veja [LICENSE](LICENSE)

---

## 🤝 Contributing

1. Fork o repo
2. Crie branch: `git checkout -b feature/sua-feature`
3. Commit: `git commit -m "feat: descrição"`
4. Push: `git push origin feature/sua-feature`
5. Abra PR

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

---

<div align="center">

**⭐ Se curtiu, deixa uma star! ⭐**

Feito com ❤️ em 🇧🇷

</div>
