# 📚 FAQ - Perguntas Frequentes

## 🚀 Setup & Configuration

### P: Preciso de quais credenciais para rodar localmente?
**R:** Você precisa de:
- Banco de dados (Supabase ou PostgreSQL local)
- Google Cloud APIs (Vision + Books)
- Hugging Face Space URL + token
- Mistral API key

Veja `.env.example` para template completo.

### P: Posso rodar sem Docker?
**R:** Sim! Mas você precisa de:
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

```bash
# Backend
pip install -r requirements.txt
python -m uvicorn app.core.main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

### P: Quanto custa rodar via Vercel?
**R:** 
- **Frontend**: Grátis (GitHub integration)
- **Backend**: Vercel Pro ($20/mês) para funções >10s
- **Database**: Supabase free tier tem bastante espaço
- **APIs**: Google Cloud free trial (genro crédito)

---

## 🐛 Troubleshooting

### P: Recebo 504 Gateway Timeout
**R:** Isso pode ser por:

1. **Imagem muito grande** → reduz resolução
2. **Vercel free tier** → atualiza para Pro
3. **Chamadas à HF Space lentas** → testa direto: 
   ```bash
   curl -X POST https://seu-hf-space.com/api -F "file=@foto.jpg"
   ```
4. **Google Vision quota** → verifica limits em Cloud Console

Use o `x-request-id` do erro para correlacionar logs!

### P: Frontend mostra "blank page"
**R:** Verifica:
- DevTools → Network → há requisições a `/api/v1`?
- `VITE_API_URL` está correto?
- CORS error no console?
- Backend está respondendo? `curl localhost:8000/health`

### P: Erro 403 ao recuperar sessão antiga
**R:** O token expirou ou é inválido:
- Sessões expiram em **24h**
- Token precisa ser enviado no header: `x-session-token: <token>`
- Verifique localStorage (`livroai_historico_sessoes`)

### P: OCR retorna texto errado/em branco
**R:** Pode ser:
- **Lombada muito pequena** na imagem (YOLO detectou errado)
- **Imagem desfocada/com glare**
- **Caracteres especiais** (acentos, símbolos)
- **Google Vision API quota excedida** → limit atingido

Dica: Teste a imagem direto na [Google Cloud Console](https://cloud.google.com/vision?hl=pt-br).

---

## 📊 Performance

### P: Por que análise leva 30-60s?
**R:** Breakdown típico:

| Etapa | Tempo |
|---|---|
| Upload + YOLO no HF | 10-20s |
| Google Vision OCR | 5-10s |
| Mistral cleanup + recs | 5-10s |
| Google Books enrichment | 5-10s |
| DB operations | 1-2s |

Nota: Dependente de latência da rede e quotas de API.

### P: Como posso acelerar?
**R:** Alternativas:

1. **Cache de livros** (já fazemos)
2. **Batch YOLO** em HF (parallelizar bboxes)
3. **Mock APIs** em desenvolvimento
4. **Redis** para cache de recomendações

---

## 🔐 Segurança

### P: Minhas fotos são armazenadas permanentemente?
**R:** Não! Apenas:
- ✅ Foto original salva em Supabase Storage
- ✅ Bboxes (coordenadas) salvas em DB
- ✅ Textos OCR + títulos limpos salvos
- ❌ Deletados automaticamente em 24h (junto com sessão)

Você pode deletar manualmente via endpoint `/sessoes/{id}` com o token.

### P: Alguém consegue ver minhas análises?
**R:** Não. Porque:
- Token aleatório e único por análise
- Header `x-session-token` é obrigatório
- Sem token = erro 403
- Sessão expira = inacessível automaticamente

Equivalent a: você tem URL + senha privada para cada análise.

### P: Meus dados é enviado para onde?
**R:** 
- 📍 Foto → Supabase Storage (servidor único)
- 📍 Texto OCR → Google Vision API (processado, não armazenado)
- 📍 Títulos limpos → Mistral API (processado, não armazenado)
- 📍 Enriquecimento → Google Books API (read-only)
- 📍 Resultado final → seu DB Supabase

Tudo em HTTPS. Nada é vendido ou compartilhado.

---

## 🛠️ Desenvolvimento

### P: Como adiciono uma NEW API?
**R:** 
1. Crie schema em `app/schemas/`
2. Crie modelo em `app/models/`
3. Crie serviço em `app/services/`
4. Crie router em `app/routers/`
5. Registre em `app/core/main.py`

Exemplo: `app.include_router(meu_router, prefix="/api/v1")`

### P: Como testo endpoints localmente?
**R:**
```bash
# Via Swagger (DEBUG=true)
curl http://localhost:8000/docs

# Via curl
curl -X POST http://localhost:8000/api/v1/analise/ \
  -F "foto=@minha_estante.jpg"

# Via httpie
http -f POST localhost:8000/api/v1/analise/ foto@estante.jpg
```

### P: Qual é o estilo de código?
**R:** Seguimos:
- **Python**: PEP 8 + Type hints (ruff + mypy)
- **JavaScript**: ESLint + Prettier
- **CSS**: BEM + CSS Variables

Roda pre-commit antes de push:
```bash
pip install pre-commit
pre-commit install
```

---

## 📖 Documentação

### P: Há documentação interativa?
**R:** Sim! Quando `DEBUG=true`:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### P: Posso gerar um client SDK?
**R:** Sim! Com OpenAPI:
```bash
# JavaScript
npx @openapitools/openapi-generator-cli generate -i http://localhost:8000/openapi.json -g javascript -o ./sdks/js

# Python
openapi-python-client generate --url http://localhost:8000/openapi.json --output-dir ./sdks/python
```

---

## 🌐 Deployment

### P: Como faço deploy do meu fork?
**R:**
1. Crie conta Vercel + Supabase
2. Connecte seu GitHub no Vercel
3. Configure environment variables
4. Deploy automático em cada push!

### P: Pode rodar em Docker em produção?
**R:** Sim! Mas:
- Railway/Render são mais fáceis que gerenciar VPS
- Vercel é grátis para frontend + barato para backend
- DigitalOcean App Platform é mid-point

Veja sessão "Deployment" no README.

---

## 🤝 Contribução

### P: Como começo a contribuir?
**R:** 
1. Fork o repo
2. Leia `CONTRIBUTING.md`
3. Abra uma issue primeiro (para features)
4. Crie PR com descrição clara

### P: Quais issues são "boas para iniciantes"?
**R:** Look por labels:
- `good-first-issue`
- `help-wanted`
- `documentation`

---

## ❓ Ainda tem dúvida?

- 🐛 Bug? Abra uma [issue](https://github.com/jairo/LivroAI/issues)
- 💬 Pergunta? Use [discussions](https://github.com/jairo/LivroAI/discussions)
- 📧 Email privado: (se houver)

---

**Última atualização:** March 2026
