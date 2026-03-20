# 🔒 Política de Segurança

## Relatando Vulnerabilidades Responsavelmente

Se você descobriu uma vulnerabilidade de segurança no LivroAI, **não abra uma issue pública**. 

### Como reportar

1. **Envie um email** para: `seu_email@seu_dominio.com` (substitua)
2. **Inclua:**
   - Descrição detalhada da vulnerabilidade
   - Passos para reproduzir
   - Impacto estimado
   - Qualquer prova de conceito (se houver)

3. **Espere resposta** em até 48 horas
4. **Trabalharemos juntos** para um patch antes de disclosure público

### Exemplos de vulnerabilidades

⚠️ **Reportar privadamente:**
- SQL Injection
- Authentication bypass
- Token exposure/reuse
- CORS misconfiguration
- Credentials em logs
- RCE / Command injection

✅ **OK abrir issue pública:**
- Performance issues
- Documentação incorreta
- UI/UX bugs
- Feature requests

---

## Security Best Practices (Usando LivroAI)

Se está rodando sua instância, faça:

### 🔐 Ambiente

```bash
# Gere .env forte (não copie do exemplo!)
# Mude senhas/keys padrão
# Use secrets manager em produção
```

### 🛡️ Supabase

- [ ] Enable Row Level Security (RLS)
- [ ] Restrict storage to authenticated users
- [ ] Regular backups habilitados
- [ ] Monitor access logs

### 🌐 API

- [ ] CORS configurado apenas para seus domínios
- [ ] Rate limiting habilitado
- [ ] HTTPS enforced (redirect HTTP)
- [ ] Request ID logging para debugging

### 📝 Logs

- [ ] Nunca log tokens/passwords
- [ ] Sanitize user input em logs
- [ ] Archive logs > 30 dias
- [ ] Encrypt sensitive logs

### 🔑 Credenciais

- [ ] Nunca commite `.env`
- [ ] Rotate API keys regularmente
- [ ] Use secrets manager (Vercel's, etc)
- [ ] Monitore quota usage (fraud detection)

---

## Vulnerabilidades Conhecidas

**Nenhuma** vulnerabilidade crítica conhecida no momento.

Se encontrar uma, siga o processo acima!

---

## Dependency Security

- 🔄 Dependências atualizadas regularmente
- 🤖 GitHub dependabot ligado
- ✅ `npm audit` e `pip check` em CI/CD

Para relatar vulnerability em dependência:
1. Verifique se é do LivroAI ou da dependência
2. Se for da dependência, report ao upstream
3. Se for na forma que usamos, report conosco

---

## Compliance

LivroAI **não é compliant** com:
- HIPAA (dados médicos)
- PCI-DSS (payment data)
- GDPR (sem processo de data removal automático)

Use sob sua responsabilidade!

---

## Security Checklist para Fork/Deploy

Se está rodando seu próprio fork:

- [ ] `.env` é `.gitignore`d
- [ ] Database password é forte
- [ ] HTTPS ligado
- [ ] API keys têm scope mínimo necessário
- [ ] Logs são privados
- [ ] Backup automático ativado
- [ ] Rate limiting on `/analise/` (evita DoS)
- [ ] File upload validation (apenas JPG/PNG)

---

## Obrigado! 🙏

Segurança é responsabilidade compartilhada. Obrigado por ajudar a manter o LivroAI seguro!

---

## Contatos

- 🐙 **GitHub Issues**: Use apenas para bugs públicos
- 📧 **Email**: seu_email@seu_dominio.com
- 🔗 **Security.txt**: `/.well-known/security.txt`

---

**Última atualização:** March 2026
