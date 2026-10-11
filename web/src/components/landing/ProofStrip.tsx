const SHOTS = [
  { src: 'shot-ask.png', cap: 'the ask — rank by inhaled dose, published formula' },
  { src: 'shot-trade.png', cap: 'measured on the live engine — +0.1 min → −9.1% dose' },
  { src: 'shot-map.png', cap: 'the product — real OSM roads, hot corridor flagged' },
]

const BADGES = ['validator passed', '20/20 offline tests', 'LLM-outage safe', 'deterministic, date-tested']

export function ProofStrip() {
  return (
    <section className="proof" id="proof">
      <div className="sec-kicker">PROOF</div>
      <h2>The engine computes. The AI only <em>words it.</em></h2>
      <div className="proof-cards">
        {SHOTS.map((s) => (
          <figure className="proof-card" key={s.src}>
            <img src={s.src} alt={s.cap} />
            <figcaption>{s.cap}</figcaption>
          </figure>
        ))}
      </div>
      <div className="proof-badges">
        {BADGES.map((b) => <span className="proof-badge" key={b}>{b}</span>)}
      </div>
      <p className="sys-note">
        A “no invented facts” gate re-checks every digit the model writes against the
        engine payload — invented numbers and invented IDs are rejected, and if the LLM
        is down the template speaks instead.
      </p>
    </section>
  )
}
