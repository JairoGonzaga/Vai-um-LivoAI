# 📜 Changelog

Todas as mudanças notáveis do LivroAI serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto segue [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

### Planejado 🚀
- [ ] Suporte a múltiplos idiomas (PT-BR, EN, ES)
- [ ] Dashboard analytics (livros/mês, recomendações aceitas, etc)
- [ ] Integração Goodreads/Skoob (1-click sync)
- [ ] Modo offline (cache com service workers)
- [ ] Compartilhamento de estantes (público/privado)
- [ ] Historico de mudanças (antes/depois)

---

## [1.0.0] - 2026-03-19

### Lançamento Público 🎉

#### Adicionado
- ✅ Upload de imagem com análise multi-etapa
- ✅ Detecção com YOLO (via HF Space)
- ✅ OCR automático (Google Vision)
- ✅ Geração de recomendações (Mistral LLM)
- ✅ Enriquecimento com Google Books
- ✅ Histórico de sessões com expiração (24h)
- ✅ Catálogo pessoal com filtros
- ✅ Interface luxury design
- ✅ Segurança com token por sessão
- ✅ Deploy em Vercel (backend + frontend)
- ✅ Documentação completa
- ✅ Docker Compose para dev local

#### Corrigido
- 🐛 **504 timeout**: Limited processing scope + batch DB ops
- 🐛 **400 CORS preflight**: Middleware ordering fix + regex origin matching
- 🐛 **SQLAlchemy string attributes**: Fixed selectinload string usage → class-bound attributes
- 🐛 **Frontend API interceptor**: Removido config.metadata mutation

#### Segurança
- 🔐 CORS configurado para produção
- 🔐 Session tokens únicos por análise
- 🔐 Request ID correlation logging
- 🔐 Senha de banco em variáveis secretas

#### Performance
- ⚡ FastAPI async pipeline
- ⚡ Batch DB flushing (1 vs N operations)
- ⚡ Response time: <100ms típico (exceto I/O externo)
- ⚡ Frontend lazy loading com React hooks

---

## [0.9.0] - 2026-03-15

### Release Candidate

#### Adicionado
- Refactor completo do frontend com luxury design
- Navbar com navegação fixa
- Home com hero section + features grid
- Componentes estilizados (Upload, Cards, etc)
- CSS Variables + base styles
- Page Histórico com detalhes de análise
- Page Catálogo com agregação de livros

#### Mudado
- Remover "Ver exemplo" do hero (sem utilidade)
- Atualizar labels da Navbar (Início, Catálogo, Histórico)

#### Corrigido
- Bug na agregação de livros do histórico

---

## [0.8.0] - 2026-03-10

### Backend Otimização

#### Adicionado
- Request logging com correlation IDs
- Stage-level timing logs (YOLO, OCR, IA, DB)
- Performance instrumentation

#### Mudado
- Reduzir max livros para enrichment: 10 → 8
- Reduzir max recomendações: 10 → 6
- Batch DB flush (economia de roundtrips)

#### Corrigido
- 504 Gateway Timeout em Vercel (otimizações acima)

---

## [0.7.0] - 2026-03-05

### CORS & Middleware Fix

#### Adicionado
- CORS middleware configuration com regex
- Support para Vercel preview branches

#### Mudado
- Reordenar middleware (CORS primeiro)
- Adicionar `ALLOWED_ORIGIN_REGEX` pattern

#### Corrigido
- 400 Bad Request em preflight OPTIONS
- SQLAlchemy selectinload string → class-bound attributes

---

## [0.6.0] - 2026-03-01

### Frontend Foundation

#### Adicionado
- React + Vite setup
- Zustand store (state management)
- Axios com interceptors
- LocalStorage para histórico

#### Mudado
- Estrutura de pastas frontend

---

## [0.5.0] - 2026-02-25

### Database Schema

#### Adicionado
- SQLAlchemy ORM com async support
- Modelos: Sessao, Livro, Recomendacao, AnaliseYolo
- Migrations com Alembic

#### Mudado
- Atualizar vercel.json para Python support

---

## [0.4.0] - 2026-02-20

### API Routes

#### Adicionado
- Endpoint POST `/analise/`
- Endpoint GET `/sessoes/{id}`
- Endpoint GET `/livros`
- Health check

---

## [0.3.0] - 2026-02-15

### Serviços Externos

#### Adicionado
- YOLO integration (HF Space)
- Google Vision OCR wrapper
- Google Books enrichment
- Mistral LLM wrapper
- Supabase Storage upload

---

## [0.2.0] - 2026-02-10

### FastAPI Setup

#### Adicionado
- FastAPI framework
- Pydantic schemas
- CORS middleware
- Docker setup

---

## [0.1.0] - 2026-02-01

### Initial Commit

#### Adicionado
- README.md
- requirements.txt
- docker-compose.yml
- .env.example
- Estrutura básica de pastas

---

## Como contribuir?

Ver [CONTRIBUTING.md](CONTRIBUTING.md)

## Reportar bugs?

Abra uma [issue](https://github.com/jairo/LivroAI/issues) com template.

---

**Que vem depois?** 👀 Veja [Unreleased](#unreleased) acima!
