import { useState, useMemo } from "react";
import useResultadoStore from "../store/resultadoStore";
import styles from "./Catalogo.module.css";

export default function Catalogo() {
  const { livrosDetectados, recomendacoes, historico } = useResultadoStore();
  const [filtro, setFiltro] = useState("todos");

  // Agregar todos os livros do histórico
  const todosLivros = useMemo(() => {
    const mapa = new Map();

    historico.forEach((sessao) => {
      // Livros detectados
      sessao.livros_detectados?.forEach((livro) => {
        if (!mapa.has(livro.id)) {
          mapa.set(livro.id, {
            ...livro,
            tipo: "detectado",
            sessoes: [],
          });
        }
        const item = mapa.get(livro.id);
        if (!item.sessoes.includes(sessao.sessao_id)) {
          item.sessoes.push(sessao.sessao_id);
        }
      });

      // Recomendações
      sessao.recomendacoes?.forEach((rec) => {
        const livro = rec.livro;
        if (livro && !mapa.has(livro.id)) {
          mapa.set(livro.id, {
            ...livro,
            tipo: "recomendado",
            recomendacoes: [],
            sessoes: [],
          });
        }
        const item = mapa.get(livro.id);
        if (item.tipo !== "detectado") {
          item.tipo = "ambos";
        }
        if (rec.justificativa_ia && !item.recomendacoes) {
          item.recomendacoes = [];
        }
        if (item.recomendacoes && !item.recomendacoes.includes(rec.justificativa_ia)) {
          item.recomendacoes.push(rec.justificativa_ia);
        }
        if (!item.sessoes.includes(sessao.sessao_id)) {
          item.sessoes.push(sessao.sessao_id);
        }
      });
    });

    return Array.from(mapa.values());
  }, [historico]);

  const livrosFiltrados = useMemo(() => {
    switch (filtro) {
      case "detectados":
        return todosLivros.filter((l) => l.tipo === "detectado" || l.tipo === "ambos");
      case "recomendados":
        return todosLivros.filter((l) => l.tipo === "recomendado" || l.tipo === "ambos");
      default:
        return todosLivros;
    }
  }, [todosLivros, filtro]);

  return (
    <div className={styles.container}>
      <section className={styles.section}>
        <div className={styles.header}>
          <div>
            <h1 className="section-title">Seu catálogo</h1>
            <p className="section-sub">
              {livrosFiltrados.length} livro{livrosFiltrados.length !== 1 ? "s" : ""}
            </p>
          </div>
        </div>

        <div className={styles.filtros}>
          <button
            className={`${styles.filtroBtn} ${filtro === "todos" ? styles.ativo : ""}`}
            onClick={() => setFiltro("todos")}
          >
            Todos ({todosLivros.length})
          </button>
          <button
            className={`${styles.filtroBtn} ${filtro === "detectados" ? styles.ativo : ""}`}
            onClick={() => setFiltro("detectados")}
          >
            Detectados ({todosLivros.filter((l) => l.tipo === "detectado" || l.tipo === "ambos").length})
          </button>
          <button
            className={`${styles.filtroBtn} ${filtro === "recomendados" ? styles.ativo : ""}`}
            onClick={() => setFiltro("recomendados")}
          >
            Recomendados ({todosLivros.filter((l) => l.tipo === "recomendado" || l.tipo === "ambos").length})
          </button>
        </div>

        {livrosFiltrados.length ? (
          <div className={styles.grid}>
            {livrosFiltrados.map((livro) => (
              <div key={livro.id} className={styles.card}>
                <div className={styles.cardHeader}>
                  {livro.tipo === "ambos" && (
                    <div className={styles.badge}>Ambos</div>
                  )}
                  {livro.tipo === "detectado" && (
                    <div className={`${styles.badge} ${styles.badgeDetectado}`}>Detectado</div>
                  )}
                  {livro.tipo === "recomendado" && (
                    <div className={`${styles.badge} ${styles.badgeRecomendado}`}>Recomendado</div>
                  )}
                </div>

                <div className={styles.cardTitle}>{livro.nome}</div>

                {livro.autor && (
                  <div className={styles.cardAuthor}>{livro.autor}</div>
                )}

                {livro.descricao && (
                  <div className={styles.cardDesc}>{livro.descricao}</div>
                )}

                <div className={styles.cardFooter}>
                  <div className={styles.stats}>
                    {livro.sessoes?.length || 0} análise{(livro.sessoes?.length || 0) !== 1 ? "s" : ""}
                  </div>
                  {livro.recomendacoes?.length > 0 && (
                    <div className={styles.recReason}>
                      {livro.recomendacoes[0]}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className={styles.empty}>
            <div className={styles.emptyIcon}>📖</div>
            <p>Nenhum livro nesta categoria.</p>
            <p style={{ fontSize: "0.85rem", marginTop: "0.5rem", color: "#a09880" }}>
              Faça uma análise para adicionar livros ao seu catálogo.
            </p>
          </div>
        )}
      </section>
    </div>
  );
}
