const STORAGE_KEY = "livroai_historico_sessoes";

function getSessionStorage() {
  if (typeof window === "undefined") return null;
  try {
    return window.sessionStorage;
  } catch {
    return null;
  }
}

function getLocalStorage() {
  if (typeof window === "undefined") return null;
  try {
    return window.localStorage;
  } catch {
    return null;
  }
}

function lerStorage(storage) {
  if (!storage) return [];
  const raw = storage.getItem(STORAGE_KEY);
  if (!raw) return [];

  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function listarHistoricoSessoes() {
  const sessionStorage = getSessionStorage();
  const localStorage = getLocalStorage();
  const historicoSessao = lerStorage(sessionStorage);

  if (historicoSessao.length > 0) {
    return historicoSessao;
  }

  const historicoLegado = lerStorage(localStorage);
  if (historicoLegado.length > 0 && sessionStorage) {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(historicoLegado));
    localStorage?.removeItem(STORAGE_KEY);
  }

  return historicoLegado;
}

export function salvarSessaoNoHistorico(sessao) {
  const sessionStorage = getSessionStorage();
  if (!sessionStorage) return [];

  const atual = listarHistoricoSessoes();
  const semDuplicata = atual.filter((item) => item.sessao_id !== sessao.sessao_id);
  const proximo = [{ ...sessao, salvo_em: new Date().toISOString() }, ...semDuplicata].slice(0, 30);
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(proximo));
  return proximo;
}

export function removerSessaoDoHistorico(sessaoId) {
  const sessionStorage = getSessionStorage();
  if (!sessionStorage) return [];

  const atual = listarHistoricoSessoes();
  const proximo = atual.filter((item) => item.sessao_id !== sessaoId);
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(proximo));
  return proximo;
}

export function limparHistoricoSessoes() {
  getSessionStorage()?.removeItem(STORAGE_KEY);
}
