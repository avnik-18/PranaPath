import type { RoutesPayload } from '../types'

export function DoseCompare({ payload }: { payload: RoutesPayload }) {
  const a = payload.route_fastest.dose_ug
  const b = payload.route_healthy.dose_ug
  const t = payload.tradeoff
  if (t.same_route) return null
  const max = Math.max(a, b) || 1
  return (
    <section className="panel">
      <div className="tradeoff">
        <span className="delta up">+{t.time_extra_minutes} min</span>
        <span className="arrow">→</span>
        <span className="delta down">−{t.dose_saving_pct}% inhaled dose</span>
      </div>
      <Bar label="A" value={a} max={max} cls="bar-a" />
      <Bar label="B" value={b} max={max} cls="bar-b" />
    </section>
  )
}

function Bar({ label, value, max, cls }: { label: string; value: number; max: number; cls: string }) {
  return (
    <div className="barrow">
      <span className="barlabel">{label}</span>
      <div className="bartrack"><div className={`barfill ${cls}`} style={{ width: `${(value / max) * 100}%` }} /></div>
      <span className="barvalue">{value} µg</span>
    </div>
  )
}
