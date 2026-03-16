import UploadFoto from "../components/UploadFoto";
import LivrosDetectados from "../components/LivrosDetectados";
import RecomendacaoCard from "../components/RecomendacaoCard";
import { analiseApi } from "../services/api";
import { salvarSessaoNoHistorico } from "../services/sessao";
import useResultadoStore from "../store/resultadoStore";

export default function Home() {
  const {
    loading,
    erro,
    livrosDetectados,
    recomendacoes,
    setLoading,
    setErro,
    setResultado,
    setHistorico,
  } = useResultadoStore();

  const handleUpload = async (file) => {
    try {
      setLoading(true);
      setErro(null);

      const resultado = await analiseApi.analisarEstante(file);
      setResultado(resultado);

      const historicoAtualizado = salvarSessaoNoHistorico(resultado);
      setHistorico(historicoAtualizado);
    } catch (error) {
      const detalhe = error?.response?.data?.detail;
      setErro(typeof detalhe === "string" ? detalhe : "Falha ao analisar imagem.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <h1>LivroAI</h1>
      <UploadFoto onUpload={handleUpload} loading={loading} />
      {erro ? <p>{erro}</p> : null}
      <LivrosDetectados livros={livrosDetectados} />

      <section>
        <h2>Recomendações</h2>
        {recomendacoes.length ? (
          recomendacoes.map((item) => (
            <RecomendacaoCard key={item.id} recomendacao={item} />
          ))
        ) : (
          <p>Sem recomendações para exibir.</p>
        )}
      </section>
    </main>
  );
}
