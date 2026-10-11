export function HonestLimits() {
  return (
    <section className="limits" id="limits">
      <div className="sec-kicker">HONEST LIMITS</div>
      <h2>Real OSM roads. Real dose math. <em>Illustrative</em> pollution bands.</h2>
      <p>
        Roads and minutes: a live OpenStreetMap cut — 4,939 junctions, 5,692 segments,
        largest connected component. Dose: the deterministic published formula.
        Per-class pollution bands are modelled — live CPCB / Open-Meteo readings land
        with the AWS ring. Full ledger: <code>docs/honest-limits.md</code>.
      </p>
    </section>
  )
}
