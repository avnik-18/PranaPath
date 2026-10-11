type Props = { onOpenApp: () => void }

export function Hero(p: Props) {
  return (
    <section className="hero" id="product">
      <div className="hero-kicker"><span className="hero-dot" />DELHI · OCTOBER · BAD-AIR DAY</div>
      <h1>
        Your navigation optimises <em>time.</em><br />
        Not what your <span className="hl">lungs get.</span>
      </h1>
      <p className="hero-sub">
        Two streets, same destination. The fastest app walks you past the market corridor
        every time. EcoRoute ranks routes by <b>inhaled dose</b> —
        measured on a real OpenStreetMap corridor, a recent demo delivered
        <b> +0.1 min → −9.1% dose</b> per trip.
      </p>
      <div className="hero-ctas">
        <button className="l-open big" onClick={p.onOpenApp}>Open the app →</button>
        <a className="hero-ghost" href="#system">See the system ↓</a>
      </div>
    </section>
  )
}
