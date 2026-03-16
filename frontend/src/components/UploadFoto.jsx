import { useState } from "react";

export default function UploadFoto({ onUpload, loading = false }) {
  const [arquivo, setArquivo] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!arquivo || loading) return;
    await onUpload(arquivo);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        accept="image/*"
        onChange={(event) => setArquivo(event.target.files?.[0] ?? null)}
      />
      <button type="submit" disabled={!arquivo || loading}>
        {loading ? "Analisando..." : "Analisar estante"}
      </button>
    </form>
  );
}
