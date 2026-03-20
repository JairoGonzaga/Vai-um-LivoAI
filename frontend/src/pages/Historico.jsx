import { useMemo, useState } from "react";
import useResultadoStore from "../store/resultadoStore";
import {
  limparHistoricoSessoes,
  listarHistoricoSessoes,
  removerSessaoDoHistorico,
} from "../services/sessao";
import { sessoesApi } from "../services/api";
import RecomendacaoCard from "../components/RecomendacaoCard";
import LivrosDetectados from "../components/LivrosDetectados";
import styles from "./Historico.module.css";

const UUID_REGEX =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

function formatarData(valor) {
  if (!valor) return "Data indisponível";
  const data = new Date(valor);
  if (Number.isNaN(data.getTime())) return "Data indisponível";
  return data.toLocaleString("pt-BR");
}

export default function Historico() {
  const { historico, setHistorico } = useResultadoStore();
  const [detalhe, setDetalhe] = useState(null);
  const [erro, setErro] = useState(null);
  const [carregandoSessaoId, setCarregandoSessaoId] = useState(null);
  const [origemDetalhe, setOrigemDetalhe] = useState("local");

  const recarregar = () => setHistorico(listarHistoricoSessoes());

  const historicoOrdenado = useMemo(() => {
    return [...historico].sort((a, b) => {
      const dataA = new Date(a?.salvo_em ?? 0).getTime();
      const dataB = new Date(b?.salvo_em ?? 0).getTime();
      return dataB - dataA;
    });
  }, [historico]);

  const abrirSessao = async (item) => {
    const sessaoId = item?.sessao_id;
    if (!sessaoId) {
      setErro("Sessão inválida no histórico.");
      return;
    }

    setDetalhe(item);
    setOrigemDetalhe("local");

    if (!UUID_REGEX.test(sessaoId)) {
      setErro("Sessão com ID inválido no histórico local.");
      return;
    }

    try {
      setErro(null);
      setCarregandoSessaoId(sessaoId);

      const status = await sessoesApi.validarSessao(sessaoId);
      if (!status?.valida) {
        setErro("Sessão expirada no servidor. Exibindo cópia salva no histórico.");
        return;
      }

      const data = await sessoesApi.buscarSessao(sessaoId);
      setDetalhe({ ...item, ...data });
      setOrigemDetalhe("api");
    } catch {
      setErro("Não foi possível sincronizar com o servidor. Exibindo cópia salva no histórico.");
    } finally {
      setCarregandoSessaoId(null);
    }
  };

  const remover = (sessaoId) => {
    const atualizado = removerSessaoDoHistorico(sessaoId);
    setHistorico(atualizado);
    if (detalhe?.sessao_id === sessaoId) setDetalhe(null);
  };

  const limparHistorico = () => {
    limparHistoricoSessoes();
    setHistorico([]);
    setDetalhe(null);
    setErro(null);
  };

  const livros = detalhe?.livros_detectados ?? [];
  const recomendacoes = detalhe?.recomendacoes ?? [];

  return (
    <main className={styles.page}>
      <section className="section">
        <span className="section-label">Sessões salvas</span>
        <h1 className="section-title">Histórico</h1>

        <div className={styles.actions}>
          <button type="button" className="btn-ghost" onClick={recarregar}>
            Atualizar
          </button>
          <button type="button" className="btn-ghost" onClick={limparHistorico}>
            Limpar histórico
          </button>
        </div>

        {erro ? <div className={styles.error}>{erro}</div> : null}

        {historicoOrdenado.length ? (
          <div className={styles.grid}>
            {historicoOrdenado.map((item) => {
              const id = item?.sessao_id ?? "sem-id";
              const selecionada = detalhe?.sessao_id === id;
              const loading = carregandoSessaoId === id;

              return (
                <article
                  key={id}
                  className={`${styles.card} ${selecionada ? styles.cardAtivo : ""}`}
                >
                  <div className={styles.cardHeader}>
                    <strong>Sessão</strong>
                    <span>{formatarData(item?.salvo_em)}</span>
                  </div>

                  <div className={styles.sessaoId}>{id}</div>

                  <div className={styles.cardStats}>
                    <span>{item?.livros_detectados?.length ?? 0} livros</span>
                    <span>{item?.recomendacoes?.length ?? 0} recomendações</span>
                  </div>

                  <div className={styles.cardActions}>
                    <button
                      type="button"
                      className="btn-primary"
                      onClick={() => abrirSessao(item)}
                      disabled={loading}
                    >
                      {loading ? "Sincronizando..." : "Abrir"}
                    </button>
                    <button
                      type="button"
                      className="btn-ghost"
                      onClick={() => remover(id)}
                    >
                      Remover
                    </button>
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <p className="section-sub">Nenhuma sessão no histórico.</p>
        )}
      </section>

      {detalhe ? (
        <section className="section">
          <span className="section-label">Detalhe da sessão</span>
          <h2 className="section-title">Sessão selecionada</h2>
          <p className="section-sub">
            Origem dos dados: {origemDetalhe === "api" ? "Servidor" : "Histórico local"}
          </p>
          <LivrosDetectados livros={livros} />

          <section className={styles.recomendacoes}>
            <h3>Recomendações</h3>
            {recomendacoes.length ? (
              <div className={styles.recomendacoesLista}>
                {recomendacoes.map((item, idx) => (
                  <RecomendacaoCard key={item.id ?? `${item.livro_id}-${idx}`} recomendacao={item} index={idx + 1} />
                ))}
              </div>
            ) : (
              <p className="section-sub">Sem recomendações para esta sessão.</p>
            )}
          </section>
        </section>
      ) : null}
    </main>
  );
}
