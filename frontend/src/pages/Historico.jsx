import { useState } from "react";
import useResultadoStore from "../store/resultadoStore";
import { listarHistoricoSessoes, removerSessaoDoHistorico } from "../services/sessao";
import { sessoesApi } from "../services/api";
import styles from "./Historico.module.css";

export default function Historico() {
  const { historico, setHistorico } = useResultadoStore();
  const [detalhe, setDetalhe] = useState(null);
  const [erro, setErro] = useState(null);
  const [carregando, setCarregando] = useState(false);

  const recarregar = () => setHistorico(listarHistoricoSessoes());

  const abrirSessao = async (item) => {
    try {
      setErro(null);
      setCarregando(true);
      const data = await sessoesApi.buscarSessao(item.sessao_id, item.token);
      setDetalhe(data);
    } catch (err) {
      const detalhe = err?.response?.data?.detail || "Não foi possível carregar a sessão.";
      setErro(detalhe);
    } finally {
      setCarregando(false);
    }
  };

  const remover = (sessaoId) => {
    const atualizado = removerSessaoDoHistorico(sessaoId);
    setHistorico(atualizado);
    if (detalhe?.sessao_id === sessaoId) setDetalhe(null);
  };

  const formatarData = (isoString) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return isoString;
    }
  };

  return (
    <div className={styles.container}>
      <section className={styles.section}>
        <div className={styles.header}>
          <div>
            <h1 className="section-title">Histórico de sessões</h1>
            <p className="section-sub">
              {historico.length} análise{historico.length !== 1 ? "s" : ""} realizada{historico.length !== 1 ? "s" : ""}
            </p>
          </div>
          <button className="btn-primary" onClick={recarregar}>
            Atualizar
          </button>
        </div>

        {historico.length ? (
          <div className={styles.list}>
            {historico.map((item) => (
              <div key={item.sessao_id} className={styles.item}>
                <div className={styles.itemInfo}>
                  <div className={styles.itemDate}>
                    {formatarData(item.salvo_em)}
                  </div>
                  <div className={styles.itemId}>
                    {item.sessao_id}
                  </div>
                  <div className={styles.itemStats}>
                    {item.livros_detectados?.length || 0} livro{item.livros_detectados?.length !== 1 ? "s" : ""} · {item.recomendacoes?.length || 0} recomendação{item.recomendacoes?.length !== 1 ? "ões" : ""}
                  </div>
                </div>
                <div className={styles.itemActions}>
                  <button
                    className={styles.btnSmall}
                    onClick={() => abrirSessao(item)}
                    disabled={carregando}
                  >
                    {carregando ? "Carregando..." : "Ver"}
                  </button>
                  <button
                    className={`${styles.btnSmall} ${styles.btnSmallDanger}`}
                    onClick={() => remover(item.sessao_id)}
                  >
                    Remover
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className={styles.empty}>
            <div className={styles.emptyIcon}>📚</div>
            <p>Nenhuma sessão no histórico.</p>
            <p style={{ fontSize: "0.85rem", marginTop: "0.5rem", color: "#a09880" }}>
              Faça uma análise para ver o histórico aqui.
            </p>
          </div>
        )}

        {erro && (
          <div className={styles.errorBox}>
            {erro}
          </div>
        )}

        {detalhe && (
          <div className={styles.detalheSection}>
            <div className={styles.detalheHeader}>
              <div className={styles.detalheTitle}>
                Detalhes da análise
              </div>
              <button
                className={styles.detalheClose}
                onClick={() => setDetalhe(null)}
              >
                ✕
              </button>
            </div>

            <div className={styles.detalheCol}>
              <div className={styles.detalheCard}>
                <span className={styles.detalheLabel}>ID da sessão</span>
                <div className={styles.detalheValue} style={{ fontSize: "0.75rem", wordBreak: "break-all" }}>
                  {detalhe.sessao_id}
                </div>
              </div>
              <div className={styles.detalheCard}>
                <span className={styles.detalheLabel}>Livros detectados</span>
                <div className={styles.detalheValue}>
                  {detalhe.livros_detectados?.length || 0}
                </div>
              </div>
              <div className={styles.detalheCard}>
                <span className={styles.detalheLabel}>Recomendações</span>
                <div className={styles.detalheValue}>
                  {detalhe.recomendacoes?.length || 0}
                </div>
              </div>
            </div>

            {detalhe.livros_detectados?.length > 0 && (
              <div>
                <h3 style={{ marginBottom: "1rem", fontSize: "1.1rem" }}>Livros detectados</h3>
                <div className={styles.detalheLista}>
                  {detalhe.livros_detectados.map((livro) => (
                    <div key={livro.id} className={styles.detalheItem}>
                      <div className={styles.detalheItemTitle}>{livro.nome}</div>
                      {livro.autor && (
                        <div className={styles.detalheItemAuthor}>{livro.autor}</div>
                      )}
                      {livro.descricao && (
                        <div className={styles.detalheItemText}>{livro.descricao}</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {detalhe.recomendacoes?.length > 0 && (
              <div style={{ marginTop: "1.5rem" }}>
                <h3 style={{ marginBottom: "1rem", fontSize: "1.1rem" }}>Recomendações</h3>
                <div className={styles.detalheLista}>
                  {detalhe.recomendacoes.map((rec, idx) => (
                    <div key={rec.id} className={styles.detalheItem}>
                      <div style={{ marginBottom: "0.4rem", fontSize: "0.85rem", color: "#e8c97a" }}>
                        #{String(idx + 1).padStart(2, "0")}
                      </div>
                      <div className={styles.detalheItemTitle}>{rec.livro?.nome}</div>
                      {rec.livro?.autor && (
                        <div className={styles.detalheItemAuthor}>{rec.livro.autor}</div>
                      )}
                      {rec.justificativa_ia && (
                        <div className={styles.detalheItemText}>{rec.justificativa_ia}</div>
                      )}
                      {rec.tipo_recomendacao && (
                        <div style={{ marginTop: "0.4rem", fontSize: "0.75rem" }}>
                          <span style={{
                            display: "inline-block",
                            border: "1px solid rgba(255,245,220,0.18)",
                            padding: "0.18rem 0.5rem",
                            color: "#a09880",
                            letterSpacing: "0.08em",
                            textTransform: "uppercase",
                          }}>
                            {rec.tipo_recomendacao}
                          </span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
}
