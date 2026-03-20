# 🤝 Guia de Contribuição

Obrigado por querer contribuir para o **LivroAI**! Aqui estão algumas diretrizes para nos ajudar a manter o projeto organizado.

## 🎯 Como começar

1. **Fork o repositório** em GitHub
2. **Clone seu fork**:
   ```bash
   git clone https://github.com/seu-usuario/LivroAI.git
   git remote add upstream https://github.com/jairo/LivroAI.git
   ```
3. **Crie uma branch para sua feature**:
   ```bash
   git checkout -b feature/sua-feature-aqui
   ```

## 📋 Antes de abrir um PR

- [ ] Fez testes localmente com `docker compose up`?
- [ ] Atualizou o README se necessário?
- [ ] Seguiu o estilo de código do projeto?
- [ ] Testou no mobile (responsividade)?
- [ ] Seus commits têm mensagens claras?

## 🐛 Encontrou um bug?

1. **Verifique se já foi reportado**: https://github.com/jairo/LivroAI/issues
2. **Abra uma issue** descrevendo:
   - O que esperava acontecer
   - O que realmente aconteceu
   - Passos para reproduzir
   - Screenshots/logs se houver

## ✨ Quer adicionar uma feature?

1. **Abra uma issue first** descrevendo a ideia
2. Aguarde feedback dos mantenedores
3. Desenvolva a feature em sua branch
4. Abra o PR linkando a issue: `Closes #123`

## 📝 Padrão de código

### Backend (Python)

```python
# Type hints obrigatórios
def processar_livro(livro_id: UUID, titulo: str) -> LivroResponse:
    """Descrição clara do que a função faz."""
    pass

# Imports organizados
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Variáveis em snake_case
titulo_limpo = "The Great Gatsby"
```

Rodamos **ruff** e **mypy** no CI. Teste localmente:
```bash
pip install ruff mypy
ruff check .
mypy app/
```

### Frontend (JavaScript/JSX)

```javascript
// Componentes em PascalCase
export default function UploadFoto({ onUpload, loading }) {
  // Event handlers em camelCase
  const handleChange = () => {}
  
  return (
    <button onClick={handleChange}>
      {loading ? "Carregando..." : "Enviar"}
    </button>
  )
}
```

### Estilos

- Use **CSS Modules** quando possível
- Mantenha **variáveis CSS** em `globals.css`
- Mobile-first (media queries para desktop)

```css
/* Variáveis -->
:root {
  --spacing: 1rem;
  --accent: #e8c97a;
}

/* Mobile primeiro -->
.card { padding: 1rem; }

@media (min-width: 768px) {
  .card { padding: 2rem; }
}
```

## 🚀 Processo de review

1. Mantenedor revisa seu PR
2. Se houver mudanças solicitadas, faça um update e push novamente
3. Após aprovação, será merged em `main`
4. Deploy automático em Vercel

## 📚 Estrutura esperada do PR

```markdown
## Descrição
Breve resumo do que foi mudado

## Tipo de mudança
- [ ] Bug fix
- [ ] Feature nova
- [ ] Breaking change
- [ ] Documentação

## Como testar
1. ...
2. ...

## Screenshots (se UI)
[anexar imagem]

## Checklist
- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Sem console.errors
```

## 🚫 O que NÃO fazer

- ❌ Committar `.env` ou credenciais
- ❌ Misturar múltiplas features em um PR
- ❌ Rewritten commits no `main` (use merge commits)
- ❌ Targets de produção em beta features
- ❌ Dependencies sem justificativa

## 💬 Dúvidas?

- 💼 LinkedIn: [seu-link]
- 📧 Email: seu@email.com
- 🐙 Issues: Abra uma issue com a tag `question`

---

**Obrigado por contribuir! 🎉**

Todo PR, issue ou feedback é valioso para a comunidade.
