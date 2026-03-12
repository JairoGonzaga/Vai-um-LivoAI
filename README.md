<div align="center">

# 📚 LivroAI

### Um novo modo de encontrar livros em um click

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b)
![React](https://img.shields.io/badge/React-18+-61dafb)

</div>

---

## 💡 Sobre o projeto

**LivroAI** é uma aplicação que combina visão computacional e inteligência artificial para transformar a forma como você descobre novos livros.

Tire uma foto da sua estante — o sistema detecta automaticamente os livros, monta seu perfil de leitor e gera recomendações personalizadas com base no que você já leu.

> Projeto de portfólio desenvolvido para explorar a integração entre YOLOv8, LLMs e uma stack moderna de desenvolvimento web.

---

## ✨ Funcionalidades

- 📸 **Scan da estante** — fotografe seus livros e deixe a IA identificá-los automaticamente via YOLOv8
- 🤖 **Recomendações inteligentes** — sugestões personalizadas geradas por LLM com base no seu histórico de leitura
- 📖 **Gestão da estante** — organize seus livros por status: quero ler, lendo e lido
- ⭐ **Avaliações e feedback** — avalie seus livros e ajude a IA a melhorar as recomendações
- 🔄 **Modelo evolutivo** — os dados validados pelos usuários alimentam o retreino contínuo do modelo YOLO

---

## 🧱 Stack

| Camada | Tecnologia | Motivo |
|---|---|---|
| Frontend | React + Vite | SPA rápida com experiência fluida |
| Backend | FastAPI + SQLAlchemy async | Alta performance para operações de IA |
| Banco de dados | Supabase (PostgreSQL) | Auth, RLS e Storage em uma única plataforma |
| Visão computacional | YOLOv8 | Detecção de objetos estado da arte |
| IA | LLM via API | Identificação e recomendação de livros |

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                        React                            │
│         (leitura direta via Supabase client)            │
└────────────────────┬────────────────────────────────────┘
                     │ operações com lógica de negócio
                     ▼
┌─────────────────────────────────────────────────────────┐
│                      FastAPI                            │
│         YOLO · LLM · Recomendações · Storage            │
└────────────────────┬────────────────────────────────────┘
                     │ service key (bypassa RLS)
                     ▼
┌─────────────────────────────────────────────────────────┐
│                     Supabase                            │
│         PostgreSQL · Auth · Storage · RLS               │
└─────────────────────────────────────────────────────────┘
```

O React lê dados diretamente do Supabase para operações simples. Toda escrita e lógica de negócio passa pelo FastAPI, que usa a service key para operar com segurança no banco.

---

## 🗄️ Modelo de dados

```
livros ◄──── estante ────► users
  │                          │
  └──── recomendacoes ───────┘
  
users ──── analise_yolo
```

| Tabela | Descrição |
|---|---|
| `livros` | Catálogo central de livros |
| `users` | Perfis e preferências dos leitores |
| `estante` | Relação usuário ↔ livro com status e avaliação |
| `recomendacoes` | Sugestões geradas pela IA com justificativa |
| `analise_yolo` | Imagens e detecções para retreino do modelo |

---

## 🔄 Fluxo principal

```
📸 Foto da estante
    ↓
🔍 YOLOv8 detecta os livros
    ↓
🧠 LLM identifica e enriquece os dados
    ↓
💾 Livros salvos na estante do usuário
    ↓
✨ IA gera recomendações personalizadas
    ↓
👍 Usuário dá feedback → modelo melhora
```

---

## 📁 Estrutura do projeto

```
livroai/
├── backend/
│   └── app/
│       ├── core/           # config, database, auth, main
│       ├── models/         # SQLAlchemy ORM
│       ├── schemas/        # Pydantic (request/response)
│       ├── routers/        # endpoints por domínio
│       └── services/       # YOLO, LLM, Storage
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/       # supabase client + api axios
│       ├── hooks/
│       └── store/          # Zustand
│
├── supabase/
│   └── migrations/         # SQL migrations
│
└── ml/
    ├── models/             # pesos YOLO (.pt)
    ├── dataset/            # imagens + labels validados
    └── scripts/            # export dataset + treino
```

---

## 🚧 Status do desenvolvimento

### ✅ Concluído
- Schema completo do banco de dados
- Migrations SQL com RLS, índices e triggers
- `core/` — config, database e main do FastAPI
- `models/` — todos os models SQLAlchemy
- `schemas/` — Pydantic schemas

### 🔜 Em andamento
- `routers/` — endpoints da API
- `core/auth.py` — validação JWT via Supabase JWKS
- `services/` — YOLO, LLM e Storage
- Frontend React

---

## ⚙️ Como rodar localmente

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Conta no [Supabase](https://supabase.com)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha com suas credenciais
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # preencha com suas credenciais
npm run dev
```

---

