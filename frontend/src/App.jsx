import { useState } from "react";
import Home from "./pages/Home";
import Historico from "./pages/Historico";

export default function App() {
  const [pagina, setPagina] = useState("home");

  return (
    <div>
      <header>
        <nav>
          <button type="button" onClick={() => setPagina("home")}>
            Home
          </button>
          <button type="button" onClick={() => setPagina("historico")}>
            Histórico
          </button>
        </nav>
      </header>
      {pagina === "home" ? <Home /> : <Historico />}
    </div>
  );
}
