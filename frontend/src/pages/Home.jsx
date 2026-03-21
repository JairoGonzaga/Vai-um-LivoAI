import { useEffect, useRef, useState } from "react";
import UploadFoto from "../components/UploadFoto";
import LivrosDetectados from "../components/LivrosDetectados";
import RecomendacaoCard from "../components/RecomendacaoCard";
import { analiseApi, setRuntimeAuthToken } from "../services/api";
import { salvarSessaoNoHistorico } from "../services/sessao";
import useResultadoStore from "../store/resultadoStore";
import styles from './Home.module.css';

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

  const [step, setStep] = useState(0);
  const abortControllerRef = useRef(null);

  useEffect(() => {
    return () => {
      abortControllerRef.current?.abort();
    };
  }, []);

  const handleUpload = async (file) => {
    let progressInterval;
    const abortController = new AbortController();
    abortControllerRef.current = abortController;

    try {
      setLoading(true);
      setErro(null);
      setStep(0);

      // Simula progresso visual
      progressInterval = setInterval(() => {
        setStep(prev => (prev < 5 ? prev + 1 : 5));
      }, 1200);

      const resultado = await analiseApi.analisarEstante(file, {
        signal: abortController.signal,
      });

      if (resultado?.session_token) {
        setRuntimeAuthToken(resultado.session_token);
      }
      
      clearInterval(progressInterval);
      setStep(5);

      setResultado(resultado);
      const totalLivros = resultado?.livros_detectados?.length ?? 0;
      const totalRecomendacoes = resultado?.recomendacoes?.length ?? 0;

      if (totalLivros === 0 && totalRecomendacoes === 0) {
        setErro(
          "Não conseguimos identificar títulos válidos nesta foto. Tente novamente com melhor iluminação, mantendo as lombadas retas e evitando livros muito finos ou parcialmente cobertos."
        );
      }

      const historicoAtualizado = salvarSessaoNoHistorico(resultado);
      setHistorico(historicoAtualizado);

      setTimeout(() => setStep(0), 500);
    } catch (error) {
      const isTimeout = error?.code === "ECONNABORTED";
      const isCanceled =
        error?.code === "ERR_CANCELED" ||
        error?.name === "CanceledError" ||
        error?.name === "AbortError";
      const status = error?.response?.status;
      const detalhe = error?.response?.data?.detail;
      const vercelRequestId = error?.response?.headers?.["x-vercel-id"];
      const requestId =
        error?.response?.headers?.["x-request-id"] ??
        error?.config?.headers?.["x-client-request-id"];

      if (import.meta.env.DEV) {
        console.error("Falha no upload/análise", {
          status,
          detalhe,
          vercelRequestId,
          requestId,
          data: error?.response?.data,
        });
      }

      if (isCanceled) {
        setErro("Análise cancelada.");
      } else if (typeof detalhe === "string" && detalhe.trim()) {
        setErro(detalhe);
      } else if (status === 413) {
        setErro("A imagem está grande demais para envio. Tente uma foto mais próxima da estante ou com menor resolução.");
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
      setStep(0);
    } finally {
      if (progressInterval) {
        clearInterval(progressInterval);
      }
      abortControllerRef.current = null;
      setLoading(false);
    }
  };

  const cancelarAnalise = () => {
    abortControllerRef.current?.abort();
    setStep(0);
  };

  const resetDemo = () => {
    setResultado(null);
    setErro(null);
    setStep(0);
  };

  return (
    <div className={styles.container}>
      {/* HERO */}
      <section className={styles.hero}>
        <div className={styles.heroEyebrow}>
          <span className={styles.eyebrowDot}>●</span>
          Inteligência artificial literária
        </div>
        <h1 className={styles.heroTitle}>
          Sua estante conta<br />
          <em>histórias que você ainda</em><br />
          não leu
        </h1>
        <p className={styles.heroSub}>
          Fotografe seus livros. Nossa IA detecta os títulos, entende seu gosto e recomenda o que você vai amar ler a seguir.
        </p>
        <div className={styles.heroActions}>
          <button 
            className="btn-primary" 
            onClick={() => document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' })}
          >
            Analisar minha estante
          </button>
        </div>

        {/* Decorative spines */}
        <div className={styles.spines}>
          {[180, 160, 200, 140, 190, 150, 175, 165, 195, 155, 185, 145, 170, 160, 200, 175, 155, 190].map((h, i) => (
            <div
              key={i}
              className={styles.spine}
              style={{
                height: `${h}px`,
              }}
            />
          ))}
        </div>

        <div className={styles.heroScroll}>
          <div className={styles.scrollLine}></div>
          <span>scroll</span>
        </div>
      </section>

      {/* FEATURES */}
      <section className={styles.section}>
        <span className="section-label">O que fazemos</span>
        <h2 className={styles.sectionTitle}>Do pixel ao parágrafo,<br />em segundos</h2>
        <div className={styles.featuresGrid}>
          <div className={styles.featureCell}>
            <div className={styles.featureIcon}>📸</div>
            <div className={styles.featureTitle}>Detecção visual</div>
            <p className={styles.featureDesc}>
              YOLO identifica cada livro na sua foto, extraindo com precisão as regiões de cada lombada.
            </p>
          </div>
          <div className={styles.featureCell}>
            <div className={styles.featureIcon}>🔎</div>
            <div className={styles.featureTitle}>OCR inteligente</div>
            <p className={styles.featureDesc}>
              Google Vision lê os títulos em cada recorte. Mesmo com lombadas tortas ou iluminação ruim.
            </p>
          </div>
          <div className={styles.featureCell}>
            <div className={styles.featureIcon}>✨</div>
            <div className={styles.featureTitle}>Recomendações por IA</div>
            <p className={styles.featureDesc}>
              Mistral analisa seu perfil de leitura e sugere livros que realmente combinam com você.
            </p>
          </div>
        </div>
      </section>

      <hr />

      {/* DEMO SECTION */}
      <section className={styles.demoSection} id="demo">
        {/* UPLOAD STATE */}
        {!loading && livrosDetectados.length === 0 && (
          <div className={styles.section}>
            <span className="section-label">Análise de estante</span>
            <div className="two-col">
              <div>
                <h2 className={styles.sectionTitle}>Foto a foto,<br />leitura a leitura</h2>
                <p className="section-sub">
                  Envie uma foto clara da sua estante. O processamento leva cerca de 30 a 60 segundos.
                </p>
              </div>
              <div>
                <UploadFoto onUpload={handleUpload} loading={loading} />
                <div className={styles.tipsBox}>
                  <h3 className={styles.tipsTitle}>Dicas para melhorar o resultado</h3>
                  <ul className={styles.tipsList}>
                    <li>Use boa iluminação e evite reflexos na lombada.</li>
                    <li>Mantenha a câmera reta e a estante inteira no enquadramento.</li>
                    <li>Evite livros extremamente finos, sobrepostos ou cobertos por objetos.</li>
                    <li>Chegue um pouco mais perto para deixar os títulos legíveis.</li>
                  </ul>
                </div>
              </div>
            </div>
            {erro && <div className={styles.errorBox}>{erro}</div>}
          </div>
        )}

        {/* LOADING STATE */}
        {loading && (
          <div className={styles.section}>
            <span className="section-label">Processando</span>
            <h2 className={styles.sectionTitle}>Analisando sua estante…</h2>
            <button className="btn-ghost" onClick={cancelarAnalise}>Cancelar análise</button>
            <div style={{ maxWidth: '480px' }}>
              <div className={styles.progressSteps}>
                {[
                  'Segmentação de objetos com YOLO',
                  'OCR nas lombadas detectadas',
                  'Limpeza de títulos com Mistral',
                  'Enriquecimento via Google Books',
                  'Gerando recomendações personalizadas',
                ].map((label, idx) => (
                  <div
                    key={idx}
                    className={`${styles.step} ${
                      idx < step ? styles.done : idx === step ? styles.active : ''
                    }`}
                  >
                    <div className={styles.stepDot}></div>
                    <span>{label}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* RESULTS STATE */}
        {!loading && livrosDetectados.length > 0 && (
          <div className={styles.section}>
            <span className="section-label">Sessão ativa</span>
            <div className="two-col">
              <div>
                <h2 className={styles.sectionTitle}>Livros<br />detectados</h2>
                <p className="section-sub">
                  {livrosDetectados.length} livros encontrados na sua estante. Clique em qualquer um para mais detalhes.
                </p>
                <LivrosDetectados livros={livrosDetectados} />
              </div>
              <div>
                <h2 className={styles.sectionTitle}>Recomendações<br />para você</h2>
                <p className="section-sub">
                  Baseado no seu perfil de leitura, nossa IA selecionou:
                </p>
                {recomendacoes.length > 0 ? (
                  <div className={styles.recList}>
                    {recomendacoes.map((item, idx) => (
                      <RecomendacaoCard key={item.id} recomendacao={item} index={idx + 1} />
                    ))}
                  </div>
                ) : (
                  <p className="section-sub">Sem recomendações para exibir.</p>
                )}
              </div>
            </div>
            <div className={styles.resultFooter}>
              <button className="btn-ghost" onClick={resetDemo}>Nova análise</button>
              <button className="btn-primary">Salvar sessão</button>
            </div>
          </div>
        )}
      </section>

      {/* FOOTER */}
      <footer className={styles.footer}>
        <div className={styles.footerLogo}>LivroAI</div>
        <span>Powered by YOLO · Google Vision · Mistral · Supabase</span>
        <span>© 2025</span>
      </footer>
    </div>
  );
}
