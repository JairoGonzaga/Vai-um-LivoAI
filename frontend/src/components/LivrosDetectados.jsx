export default function LivrosDetectados({ livros = [] }) {
  if (!livros.length) {
    return <p>Nenhum livro detectado ainda.</p>;
  }

  return (
    <section>
      <h2>Livros detectados</h2>
      <ul>
        {livros.map((livro) => (
          <li key={livro.id}>
            <strong>{livro.nome}</strong>
            {livro.autor ? <span> — {livro.autor}</span> : null}
          </li>
        ))}
      </ul>
    </section>
  );
}
