import styles from "./RecomendacaoCard.module.css";

export default function RecomendacaoCard({ recomendacao, index = 1 }) {
  const livro = recomendacao?.livro;

  return (
    <div className={styles.item}>
      <div className={styles.num}>{String(index).padStart(2, "0")}</div>
      <div className={styles.content}>
        <div className={styles.title}>{livro?.nome ?? "Livro recomendado"}</div>
        {livro?.autor && (
          <div className={styles.author}>{livro.autor}</div>
        )}
        {recomendacao?.justificativa_ia && (
          <p className={styles.reason}>{recomendacao.justificativa_ia}</p>
        )}
        {recomendacao?.tipo_recomendacao && (
          <div className={styles.tags}>
            <span className={styles.tag}>{recomendacao.tipo_recomendacao}</span>
          </div>
        )}
      </div>
    </div>
  );
}
