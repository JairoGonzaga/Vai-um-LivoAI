import styles from './Navbar.module.css';

export default function Navbar({ onNavigate }) {
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        Livro<span>AI</span>
      </div>
      <ul className={styles.navLinks}>
        <li><a onClick={() => onNavigate('home')}>Como funciona</a></li>
        <li><a onClick={() => onNavigate('home')}>Catálogo</a></li>
        <li><a onClick={() => onNavigate('historico')}>Sessões</a></li>
      </ul>
      <button 
        className={styles.navCta}
        onClick={() => document.getElementById('demo')?.scrollIntoView({ behavior: 'smooth' })}
      >
        Analisar estante
      </button>
    </nav>
  );
}
