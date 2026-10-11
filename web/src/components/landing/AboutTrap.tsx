export function AboutTrap() {
  return (
    <section className="about" id="about">
      <div className="about-copy">
        <div className="sec-kicker">THE TRAP</div>
        <h2>One street walks you past the market. <em>Every time.</em></h2>
        <p>
          Two streets lead to the same destination. One is short but grazes a dense
          market corridor; the other detours two blocks around it. The fastest route wins
          by a hair — and hands your lungs the heavier load, every trip, every runner.
        </p>
        <p>
          Maps optimise minutes. Nobody mechanically optimises what you inhale.
          So we stopped asking the map and built the number instead.
        </p>
      </div>
      <div className="about-formula">
        <div className="lbl">one honest number per street segment</div>
        <div className="mono">dose(µg) = Σ&nbsp;&nbsp;C(section) × IR(rate) ×<br />minutes(section) / 60</div>
        <div className="sub">C = pollution (µg/m³) · IR = breathing rate (m³/h)<br />
          jog 3.0 · cycle 2.3 · walk 1.4 &nbsp;— published formula, deterministic engine,
          <b> no AI touches the math</b></div>
      </div>
    </section>
  )
}
