import { useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Historico from "./pages/Historico";
import Catalogo from "./pages/Catalogo";

export default function App() {
  const [pagina, setPagina] = useState("home");

  return (
    <div>
      <Navbar currentPage={pagina} onNavigate={setPagina} />
      {pagina === "home" ? <Home /> : pagina === "historico" ? <Historico /> : <Catalogo />}
    </div>
  );
}
