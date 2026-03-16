export default function RecomendacaoCard({ recomendacao }) {
  const livro = recomendacao?.livro;

  return (
    <article>
      <h3>{livro?.nome ?? "Livro recomendado"}</h3>
      {livro?.autor ? <p>Autor: {livro.autor}</p> : null}
      {recomendacao?.tipo_recomendacao ? (
        <p>Tipo: {recomendacao.tipo_recomendacao}</p>
      ) : null}
      {recomendacao?.justificativa_ia ? <p>{recomendacao.justificativa_ia}</p> : null}
    </article>
  );
}
