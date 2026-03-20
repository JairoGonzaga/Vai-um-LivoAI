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
      const isTimeout = error?.code === "ECONNABORTED";
      const status = error?.response?.status;
      const detalhe = error?.response?.data?.detail;
      const vercelRequestId = error?.response?.headers?.["x-vercel-id"];
      const requestId =
        error?.response?.headers?.["x-request-id"] ??
        error?.config?.headers?.["x-client-request-id"];

      console.error("Falha no upload/análise", {
        status,
        detalhe,
        vercelRequestId,
        requestId,
        data: error?.response?.data,
      });

      if (typeof detalhe === "string" && detalhe.trim()) {
        setErro(detalhe);
      } else if (isTimeout) {
        setErro("A análise demorou mais do que o esperado. Tente novamente com uma imagem menor ou aguarde alguns segundos e tente de novo.");
      } else if (status) {
        setErro(
          vercelRequestId
            ? `Falha ao analisar imagem (HTTP ${status}) · req ${requestId ?? vercelRequestId}`
            : requestId
              ? `Falha ao analisar imagem (HTTP ${status}) · req ${requestId}`
              : `Falha ao analisar imagem (HTTP ${status}).`
        );
      } else {
        setErro("Falha ao analisar imagem.");
      }
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
