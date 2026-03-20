import { useRef, useState } from "react";
import styles from "./UploadFoto.module.css";

export default function UploadFoto({ onUpload, loading = false }) {
  const [arquivo, setArquivo] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      setArquivo(files[0]);
    }
  };

  const handleChange = (e) => {
    setArquivo(e.target.files?.[0] ?? null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!arquivo || loading) return;
    await onUpload(arquivo);
    setArquivo(null);
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div
        className={`${styles.uploadZone} ${dragActive ? styles.dragActive : ""}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className={styles.uploadIcon}>📸</div>
        <label className={styles.uploadLabel}>
          {arquivo ? arquivo.name : "Arraste sua foto aqui"}
        </label>
        {!arquivo && (
          <span className={styles.uploadHint}>ou clique para selecionar</span>
        )}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleChange}
          className={styles.fileInput}
        />
      </div>
      {arquivo && (
        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading}
        >
          {loading ? "Analisando..." : "Analisar estante"}
        </button>
      )}
    </form>
  );
}
