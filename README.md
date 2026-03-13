<div align="center">

# 📚 LivroAI

### Um novo modo de encontrar livros em um clique

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

- 📸 **Análise da estante por imagem** — upload de foto para detectar livros com YOLOv8
- 🤖 **Recomendações por sessão** — sugestões geradas com base nos livros detectados
- 📚 **Catálogo de livros** — consulta e criação de livros via API
- 🧩 **Sessões temporárias** — cada análise gera uma sessão com expiração

---

## 🧱 Stack

| Camada | Tecnologia | Motivo |
|---|---|---|
| Backend | FastAPI + SQLAlchemy async | Alta performance para operações de IA |
| Banco de dados | Supabase (PostgreSQL) | Persistência e consultas relacionais |
| Visão computacional | YOLOv8 | Detecção de objetos estado da arte |
| IA | LLM via API | Identificação e recomendação de livros |

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

Atualmente o projeto neste repositório está focado no backend FastAPI e no fluxo de análise/recomendação por sessão.

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
| `sessoes` | Sessões temporárias de análise e recomendação |
| `recomendacoes` | Sugestões geradas pela IA com justificativa |
| `analise_yolo` | Imagens e detecções para retreino do modelo |

---

## 🔄 Fluxo principal

```
📸 Foto da estante
    ↓
🔍 YOLOv8 detecta os livros
    ↓
🔍 OCR le os textos da capa
    ↓
🧠 LLM identifica e enriquece os dados
    ↓
💾 Dados salvos na sessão de análise
    ↓
✨ IA gera recomendações personalizadas
    ↓
👍 Usuário dá feedback → modelo melhora
```

---

## 📁 Estrutura do projeto

```
LivroAI/
├── app/
│   ├── core/               # config, database e inicialização da API
│   ├── models/             # models SQLAlchemy
│   ├── schemas/            # schemas Pydantic
│   ├── routers/            # endpoints (livros, análise, sessões)
│   └── services/           # regras de negócio
├── .env                    # variáveis de ambiente locais
└── README.md
```

---

## 🚧 Status do desenvolvimento

### ✅ Concluído
- `core/` — configuração, conexão com banco e lifecycle da API
- `models/` — entidades principais (`livros`, `sessoes`, `recomendacoes`, `analise_yolo`)
- `schemas/` — contratos de request/response
- `routers/` — rotas de livros, análise de imagem e sessões

### 🔜 Em andamento
- Integração completa dos serviços de YOLO/LLM em produção
- Evolução de qualidade de recomendação
- Camada cliente (frontend)

---

## ⚙️ Como rodar localmente

### Pré-requisitos
- Python 3.11+
- Conta no [Supabase](https://supabase.com)

### Backend

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
# instale as dependências do projeto
uvicorn app.core.main:app --reload
```

### Rotas já implementadas no código

- `GET /health` — status da API (já registrado no `main`)
- `livros` — listagem, busca por ISBN e criação
- `analise` — upload de imagem para processamento
- `sessoes` — consulta, validação e remoção de sessão

---


