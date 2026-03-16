const STORAGE_KEY = "livroai_historico_sessoes";

export function listarHistoricoSessoes() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return [];

  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function salvarSessaoNoHistorico(sessao) {
  const atual = listarHistoricoSessoes();
  const semDuplicata = atual.filter((item) => item.sessao_id !== sessao.sessao_id);
  const proximo = [{ ...sessao, salvo_em: new Date().toISOString() }, ...semDuplicata].slice(0, 30);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(proximo));
  return proximo;
}

export function removerSessaoDoHistorico(sessaoId) {
  const atual = listarHistoricoSessoes();
  const proximo = atual.filter((item) => item.sessao_id !== sessaoId);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(proximo));
  return proximo;
}

export function limparHistoricoSessoes() {
  localStorage.removeItem(STORAGE_KEY);
}
