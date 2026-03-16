import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1",
  timeout: 30000,
});

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
