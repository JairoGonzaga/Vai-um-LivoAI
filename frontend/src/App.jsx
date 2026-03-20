import { useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Historico from "./pages/Historico";

export default function App() {
  const [pagina, setPagina] = useState("home");

  return (
    <div>
      <Navbar currentPage={pagina} onNavigate={setPagina} />
      {pagina === "home" ? <Home /> : <Historico />}
    </div>
  );
}
