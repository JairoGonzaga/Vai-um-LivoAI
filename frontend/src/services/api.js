import axios from "axios";

const configuredApiUrl = (import.meta.env.VITE_API_URL ?? "").trim();

const api = axios.create({
  baseURL: configuredApiUrl || "/api/v1",
  timeout: 30000,
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
      data: error?.response?.data,
    });

    return Promise.reject(error);
  }
);

export const analiseApi = {
  async analisarEstante(file) {
    const formData = new FormData();
    formData.append("foto", file);

    const { data } = await api.post("/analise", formData, {
      headers: { "Content-Type": "multipart/form-data" },
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
