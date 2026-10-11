type Props = { onOpenApp: () => void }

export function Navigation(p: Props) {
  return (
    <header className="l-nav">
      <div className="brand">
        <span className="logo-dot" />
        <b>EcoRoute AI</b>
      </div>
      <nav className="l-nav-links">
        <a href="#product">Product</a>
        <a href="#system">System</a>
        <a href="#proof">Proof</a>
        <a href="#limits">Limits</a>
        <button className="l-open" onClick={p.onOpenApp}>Open the app →</button>
      </nav>
    </header>
  )
}
