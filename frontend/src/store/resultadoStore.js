import { create } from "zustand";
import { listarHistoricoSessoes } from "../services/sessao";

const useResultadoStore = create((set) => ({
  loading: false,
  erro: null,
  sessaoAtual: null,
  livrosDetectados: [],
  recomendacoes: [],
  historico: listarHistoricoSessoes(),

  setLoading: (loading) => set({ loading }),
  setErro: (erro) => set({ erro }),

  setResultado: (resultado) =>
    set({
      sessaoAtual: resultado?.sessao_id ?? null,
      livrosDetectados: resultado?.livros_detectados ?? [],
      recomendacoes: resultado?.recomendacoes ?? [],
      erro: null,
    }),

  setHistorico: (historico) => set({ historico }),

  limparResultado: () =>
    set({
      sessaoAtual: null,
      livrosDetectados: [],
      recomendacoes: [],
      erro: null,
    }),
}));

export default useResultadoStore;
