import styles from "./LivrosDetectados.module.css";

export default function LivrosDetectados({ livros = [] }) {
  if (!livros.length) {
    return (
      <section className={styles.section}>
        <h2 className="section-title">Livros detectados</h2>
        <div className={styles.empty}>Nenhum livro detectado ainda.</div>
      </section>
    );
  }

  return (
    <section className={styles.section}>
      <h2 className="section-title">Livros detectados</h2>
      <div className={styles.grid}>
        {livros.map((livro) => (
          <div key={livro.id} className={styles.card}>
            <div className={styles.title}>{livro.nome}</div>
            {livro.autor && (
              <div className={styles.author}>{livro.autor}</div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
