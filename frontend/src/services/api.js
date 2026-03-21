import axios from "axios";

const MAX_DIMENSAO_IMAGEM = 1600;
const TAMANHO_ALVO_BYTES = 1_500_000;
const REQUEST_TIMEOUT_MS = 20_000;
const ANALISE_TIMEOUT_MS = 45_000;

const configuredApiUrl = (import.meta.env.VITE_API_URL ?? "").trim();
const configuredApiKey = (import.meta.env.VITE_API_KEY ?? "").trim();
const isDev = Boolean(import.meta.env.DEV);

if (!configuredApiUrl) {
  throw new Error("VITE_API_URL não configurada.");
}

if (!configuredApiKey) {
  throw new Error("VITE_API_KEY não configurada.");
}

const baseURL = configuredApiUrl;
let runtimeAuthToken = "";

export function setRuntimeAuthToken(token) {
  runtimeAuthToken = (token ?? "").trim();
}

export function clearRuntimeAuthToken() {
  runtimeAuthToken = "";
}

function logWarn(message) {
  if (isDev) {
    console.warn(message);
  }
}

function logError(message, payload) {
  if (isDev) {
    console.error(message, payload);
  }
}

function getRuntimeAuthToken() {
  return runtimeAuthToken;
}

async function validarMagicBytesImagem(file) {
  if (!(file instanceof File)) {
    throw new Error("Arquivo inválido para upload.");
  }

  const assinatura = new Uint8Array(await file.slice(0, 12).arrayBuffer());
  const ehJpeg = assinatura[0] === 0xff && assinatura[1] === 0xd8 && assinatura[2] === 0xff;
  const ehPng =
    assinatura[0] === 0x89 &&
    assinatura[1] === 0x50 &&
    assinatura[2] === 0x4e &&
    assinatura[3] === 0x47 &&
    assinatura[4] === 0x0d &&
    assinatura[5] === 0x0a &&
    assinatura[6] === 0x1a &&
    assinatura[7] === 0x0a;
  const ehGif =
    assinatura[0] === 0x47 &&
    assinatura[1] === 0x49 &&
    assinatura[2] === 0x46 &&
    assinatura[3] === 0x38 &&
    (assinatura[4] === 0x37 || assinatura[4] === 0x39) &&
    assinatura[5] === 0x61;
  const ehWebp =
    assinatura[0] === 0x52 &&
    assinatura[1] === 0x49 &&
    assinatura[2] === 0x46 &&
    assinatura[3] === 0x46 &&
    assinatura[8] === 0x57 &&
    assinatura[9] === 0x45 &&
    assinatura[10] === 0x42 &&
    assinatura[11] === 0x50;

  if (!(ehJpeg || ehPng || ehGif || ehWebp)) {
    throw new Error("Formato de arquivo inválido. Envie uma imagem JPEG, PNG, GIF ou WEBP.");
  }
}

const api = axios.create({
  baseURL,
  timeout: REQUEST_TIMEOUT_MS,
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
  const token = getRuntimeAuthToken();
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

  if (token) {
    if (config.headers?.set) {
      config.headers.set("authorization", `Bearer ${token}`);
    } else {
      config.headers.authorization = `Bearer ${token}`;
    }
  }

  if (config.headers?.set) {
    config.headers.set("x-api-key", configuredApiKey);
  } else {
    config.headers = config.headers ?? {};
    config.headers["x-api-key"] = configuredApiKey;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    logError("Erro na API", {
      method: error?.config?.method,
      url: error?.config?.url,
      status: error?.response?.status,
      requestId: error?.response?.headers?.["x-request-id"],
    });

    return Promise.reject(error);
  }
);

export const analiseApi = {
  async analisarEstante(file, options = {}) {
    await validarMagicBytesImagem(file);

    const arquivoProcessado = await otimizarImagemParaUpload(file);
    const formData = new FormData();
    formData.append("foto", arquivoProcessado);

    const { data } = await api.post("/analise/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
      timeout: ANALISE_TIMEOUT_MS,
      signal: options.signal,
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
