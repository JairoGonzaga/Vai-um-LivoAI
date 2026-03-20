import axios from "axios";

const MAX_DIMENSAO_IMAGEM = 1600;
const TAMANHO_ALVO_BYTES = 1_500_000;

const configuredApiUrl = (import.meta.env.VITE_API_URL ?? "").trim();

const api = axios.create({
  baseURL: configuredApiUrl || "/api/v1",
  timeout: 30000,
});

async function otimizarImagemParaUpload(file) {
  if (!(file instanceof File) || !file.type?.startsWith("image/")) {
    return file;
  }

  const precisaOtimizar = file.size > TAMANHO_ALVO_BYTES || file.type !== "image/jpeg";
  if (!precisaOtimizar) {
    return file;
  }

  const imageUrl = URL.createObjectURL(file);

  try {
    const imagem = await new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = () => reject(new Error("Não foi possível ler a imagem para otimização"));
      img.src = imageUrl;
    });

    const larguraOriginal = imagem.naturalWidth || imagem.width;
    const alturaOriginal = imagem.naturalHeight || imagem.height;

    if (!larguraOriginal || !alturaOriginal) {
      return file;
    }

    const escala = Math.min(1, MAX_DIMENSAO_IMAGEM / Math.max(larguraOriginal, alturaOriginal));
    const larguraFinal = Math.max(1, Math.round(larguraOriginal * escala));
    const alturaFinal = Math.max(1, Math.round(alturaOriginal * escala));

    const canvas = document.createElement("canvas");
    canvas.width = larguraFinal;
    canvas.height = alturaFinal;

    const contexto = canvas.getContext("2d");
    if (!contexto) {
      return file;
    }

    contexto.drawImage(imagem, 0, 0, larguraFinal, alturaFinal);

    let qualidade = 0.86;
    let blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", qualidade));

    while (blob && blob.size > TAMANHO_ALVO_BYTES && qualidade > 0.55) {
      qualidade -= 0.08;
      blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", qualidade));
    }

    if (!blob) {
      return file;
    }

    const nomeSemExtensao = (file.name || "imagem").replace(/\.[^.]+$/, "");
    const arquivoOtimizado = new File([blob], `${nomeSemExtensao}.jpg`, {
      type: "image/jpeg",
      lastModified: Date.now(),
    });

    return arquivoOtimizado.size < file.size ? arquivoOtimizado : file;
  } finally {
    URL.revokeObjectURL(imageUrl);
  }
}

api.interceptors.request.use((config) => {
  const requestId =
    typeof crypto !== "undefined" && crypto.randomUUID
      ? crypto.randomUUID()
      : `req-${Date.now()}-${Math.floor(Math.random() * 100000)}`;

  if (config.headers?.set) {
    config.headers.set("x-client-request-id", requestId);
  } else {
    config.headers = config.headers ?? {};
    config.headers["x-client-request-id"] = requestId;
  }
  return config;
});

if (!configuredApiUrl) {
  console.warn(
    "VITE_API_URL não configurada. Usando baseURL relativa '/api/v1'."
  );
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("Erro na API", {
      method: error?.config?.method,
      url: error?.config?.url,
      baseURL: error?.config?.baseURL,
      status: error?.response?.status,
      detail: error?.response?.data?.detail,
      vercelRequestId: error?.response?.headers?.["x-vercel-id"],
      requestId:
        error?.response?.headers?.["x-request-id"] ??
        error?.config?.headers?.["x-client-request-id"],
      data: error?.response?.data,
    });

    return Promise.reject(error);
  }
);

export const analiseApi = {
  async analisarEstante(file) {
    const arquivoProcessado = await otimizarImagemParaUpload(file);
    const formData = new FormData();
    formData.append("foto", arquivoProcessado);

    const { data } = await api.post("/analise/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
      timeout: 180000,
    });

    return data;
  },
};

export const sessoesApi = {
  async buscarSessao(sessaoId) {
    const { data } = await api.get(`/sessoes/${sessaoId}`);
    return data;
  },

  async validarSessao(sessaoId) {
    const { data } = await api.get(`/sessoes/${sessaoId}/valida`);
    return data;
  },

  async deletarSessao(sessaoId) {
    await api.delete(`/sessoes/${sessaoId}`);
  },
};

export const livrosApi = {
  async listar(params = {}) {
    const { data } = await api.get("/livros", { params });
    return data;
  },

  async buscarPorIsbn(isbn) {
    const { data } = await api.get(`/livros/${isbn}`);
    return data;
  },

  async criar(payload) {
    const { data } = await api.post("/livros", payload);
    return data;
  },
};

export default api;
