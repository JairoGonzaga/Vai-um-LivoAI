import { useState } from 'react';
import styles from './Navbar.module.css';

export default function Navbar({ onNavigate }) {
  const [menuAberto, setMenuAberto] = useState(false);

  const navegarPara = (pagina) => {
    onNavigate(pagina);
    setMenuAberto(false);
  };

  const analisarEstante = () => {
    onNavigate('home');
    document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' });
    setMenuAberto(false);
  };

  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        Livro<span>AI</span>
      </div>
      <ul className={styles.navLinks}>
        <li><a onClick={() => navegarPara('home')}>Início</a></li>
        <li><a onClick={() => navegarPara('catalogo')}>Catálogo</a></li>
        <li><a onClick={() => navegarPara('historico')}>Histórico</a></li>
      </ul>
      <button 
        className={styles.navCta}
        onClick={analisarEstante}
      >
        Analisar estante
      </button>

      <button
        type="button"
        className={styles.menuToggle}
        aria-label="Abrir menu"
        onClick={() => setMenuAberto((valor) => !valor)}
      >
        ☰
      </button>

      {menuAberto ? (
        <div className={styles.mobileMenu}>
          <button type="button" onClick={() => navegarPara('home')}>Início</button>
          <button type="button" onClick={() => navegarPara('catalogo')}>Catálogo</button>
          <button type="button" onClick={() => navegarPara('historico')}>Histórico</button>
          <button type="button" className={styles.mobileCta} onClick={analisarEstante}>
            Analisar estante
          </button>
        </div>
      ) : null}
    </nav>
  );
}
