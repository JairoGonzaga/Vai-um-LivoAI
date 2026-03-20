import styles from './Navbar.module.css';

export default function Navbar({ onNavigate }) {
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        Livro<span>AI</span>
      </div>
      <ul className={styles.navLinks}>
        <li><a onClick={() => onNavigate('home')}>Início</a></li>
        <li><a onClick={() => onNavigate('catalogo')}>Catálogo</a></li>
        <li><a onClick={() => onNavigate('historico')}>Histórico</a></li>
      </ul>
      <button 
        className={styles.navCta}
        onClick={() => document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' }) || onNavigate('home')}
      >
        Analisar estante
      </button>
    </nav>
  );
}
