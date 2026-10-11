export function Footer() {
  return (
    <footer className="l-foot">
      <div className="brand">
        <span className="logo-dot" />
        <b>EcoRoute AI</b>
      </div>
      <nav>
        <a href="#about">about</a>
        <a href="#system">system</a>
        <a href="#proof">proof</a>
        <a href="#limits">limits</a>
      </nav>
      <div className="l-foot-note">
        built in one session · AI-assisted — see <code>CREDITS.md</code> · © {new Date().getFullYear()}
      </div>
    </footer>
  )
}
