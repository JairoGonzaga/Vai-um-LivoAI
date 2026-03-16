import { useState } from "react";
import useResultadoStore from "../store/resultadoStore";
import { listarHistoricoSessoes, removerSessaoDoHistorico } from "../services/sessao";
import { sessoesApi } from "../services/api";

export default function Historico() {
  const { historico, setHistorico } = useResultadoStore();
  const [detalhe, setDetalhe] = useState(null);
  const [erro, setErro] = useState(null);

  const recarregar = () => setHistorico(listarHistoricoSessoes());

  const abrirSessao = async (sessaoId) => {
    try {
      setErro(null);
      const data = await sessoesApi.buscarSessao(sessaoId);
      setDetalhe(data);
    } catch {
      setErro("Não foi possível carregar a sessão.");
    }
  };

  const remover = (sessaoId) => {
    const atualizado = removerSessaoDoHistorico(sessaoId);
    setHistorico(atualizado);
    if (detalhe?.sessao_id === sessaoId) setDetalhe(null);
  };

  return (
    <main>
      <h1>Histórico</h1>
      <button type="button" onClick={recarregar}>Atualizar</button>

      {historico.length ? (
        <ul>
          {historico.map((item) => (
            <li key={item.sessao_id}>
              <span>{item.sessao_id}</span>
              <button type="button" onClick={() => abrirSessao(item.sessao_id)}>
                Ver sessão
              </button>
              <button type="button" onClick={() => remover(item.sessao_id)}>
                Remover
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>Nenhuma sessão no histórico.</p>
      )}

      {erro ? <p>{erro}</p> : null}
      {detalhe ? (
        <section>
          <h2>Detalhe da sessão</h2>
          <pre>{JSON.stringify(detalhe, null, 2)}</pre>
        </section>
      ) : null}
    </main>
  );
}
