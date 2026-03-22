import axios from "axios";

const REQUEST_TIMEOUT_MS = 20_000;
const ANALISE_TIMEOUT_MS = 120_000;

const configuredProxyBasePath = (import.meta.env.VITE_PROXY_BASE_PATH ?? "/api/proxy").trim();
if (!configuredProxyBasePath) {
  throw new Error("VITE_PROXY_BASE_PATH não configurada.");
}

const baseURL = configuredProxyBasePath;
let runtimeAuthToken = "";

export function setRuntimeAuthToken(token) {
  runtimeAuthToken = (token ?? "").trim();
}

export function clearRuntimeAuthToken() {
  runtimeAuthToken = "";
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

api.interceptors.request.use((config) => {
  const token = getRuntimeAuthToken();

  if (token) {
    if (config.headers?.set) {
      config.headers.set("authorization", `Bearer ${token}`);
    } else {
      config.headers = config.headers ?? {};
      config.headers.authorization = `Bearer ${token}`;
    }
  }

  return config;
});

export const analiseApi = {
  async analisarEstante(file, options = {}) {
    await validarMagicBytesImagem(file);

    const formData = new FormData();
    formData.append("foto", file);

    const { data } = await api.post("", formData, {
      params: { path: "analise/" },
      headers: { "Content-Type": "multipart/form-data" },
      timeout: ANALISE_TIMEOUT_MS,
      signal: options.signal,
    });

    return data;
  },
};

export const sessoesApi = {
  async buscarSessao(sessaoId) {
    const { data } = await api.get("", { params: { path: `sessoes/${sessaoId}` } });
    return data;
  },

  async validarSessao(sessaoId) {
    const { data } = await api.get("", { params: { path: `sessoes/${sessaoId}/valida` } });
    return data;
  },

  async deletarSessao(sessaoId) {
    await api.delete("", { params: { path: `sessoes/${sessaoId}` } });
  },
};

export const livrosApi = {
  async listar(params = {}) {
    const { data } = await api.get("", { params: { path: "livros", ...params } });
    return data;
  },

  async buscarPorIsbn(isbn) {
    const { data } = await api.get("", { params: { path: `livros/${isbn}` } });
    return data;
  },

  async criar(payload) {
    const { data } = await api.post("", payload, { params: { path: "livros" } });
    return data;
  },
};

export default api;
