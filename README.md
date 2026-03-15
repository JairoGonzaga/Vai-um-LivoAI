---
title: LivroAI
emoji: 📚
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

<div align="center">

# 📚 LivroAI

### Um novo modo de encontrar livros em um clique

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b)

</div>

---

## 💡 Sobre o projeto

**LivroAI** é uma aplicação que combina visão computacional e inteligência artificial para transformar a forma como você descobre novos livros.

Tire uma foto da sua estante — o sistema detecta automaticamente os livros e gera recomendações personalizadas com base no que você já leu.

> Projeto de portfólio desenvolvido para explorar a integração entre YOLOv8, LLMs e uma stack moderna de desenvolvimento web.

---

## ✨ Funcionalidades

- 📸 **Análise da estante por imagem** — upload de foto para detectar livros com YOLOv8
- 🤖 **Recomendações por sessão** — sugestões geradas com base nos livros detectados
- 📚 **Catálogo de livros** — consulta e criação de livros via Google Books API
- 🧩 **Sessões temporárias** — cada análise gera uma sessão com expiração de 24h

---

## 🧱 Stack

| Camada | Tecnologia |
|---|---|
| Backend | FastAPI + SQLAlchemy async |
| Banco de dados | Supabase (PostgreSQL) |
| Visão computacional | YOLOv8 |
| IA | LLM via API |
| Deploy | Hugging Face Spaces (Docker) |

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                      FastAPI                            │
│      Routers · Services · YOLO · LLM · Sessões          │
└────────────────────┬────────────────────────────────────┘
                     │ SQLAlchemy async
                     ▼
┌─────────────────────────────────────────────────────────┐
│                     Supabase                            │
│            PostgreSQL · Storage · RLS                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ Modelo de dados

```
livros ◄──── recomendacoes ────► sessoes
                                    │
                                    └──── analise_yolo
```

| Tabela | Descrição |
|---|---|
| `livros` | Catálogo central de livros |
| `sessoes` | Sessões temporárias · expiram em 24h |
| `recomendacoes` | Sugestões geradas pela IA |
| `analise_yolo` | Imagens e detecções para retreino |

---

## 🔄 Fluxo principal

```
📸 Foto da estante
    ↓
🔍 YOLOv8 detecta os livros
    ↓
🧠 LLM identifica e enriquece os dados
    ↓
💾 Dados salvos na sessão de análise
    ↓
✨ IA gera recomendações personalizadas
```

---

## 🔌 API Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/v1/analise` | Envia foto → retorna livros + recomendações |
| `GET` | `/api/v1/sessoes/{id}` | Histórico da sessão |
| `GET` | `/api/v1/sessoes/{id}/valida` | Verifica se sessão está ativa |
| `DELETE` | `/api/v1/sessoes/{id}` | Remove sessão |
| `GET` | `/api/v1/livros` | Lista catálogo com filtros |
| `GET` | `/api/v1/livros/{isbn}` | Busca livro por ISBN |
| `POST` | `/api/v1/livros` | Adiciona livro via Google Books |
| `GET` | `/health` | Health check |

---

## 📁 Estrutura do projeto

```
LivroAI/
├── Dockerfile
├── requirements.txt
├── app/
│   ├── core/               # config, database e lifecycle da API
│   ├── models/             # SQLAlchemy ORM
│   ├── schemas/            # Pydantic schemas
│   ├── routers/            # endpoints
│   └── services/           # regras de negócio
└── README.md
```

---

## 🚧 Status do desenvolvimento

### ✅ Concluído
- `core/` — configuração, banco e lifecycle
- `models/` — todas as entidades
- `schemas/` — contratos de request/response
- `routers/` — livros, análise e sessões

### 🔜 Em andamento
- `services/` — YOLO, LLM, Google Books e Storage
- Frontend React
- Retreino contínuo do modelo

---

## ⚙️ Variáveis de ambiente

Configure as seguintes secrets no HF Spaces em **Settings → Variables and secrets**:

```
DATABASE_URL
SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_SERVICE_KEY
STORAGE_BUCKET_FOTOS
GOOGLE_BOOKS_API_KEY
YOLO_MODEL_PATH
APP_ENV
```