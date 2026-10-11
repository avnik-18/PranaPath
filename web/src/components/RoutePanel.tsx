import type { RoutesPayload } from '../types'

export function RoutePanel({ payload }: { payload: RoutesPayload }) {
  const a = payload.route_fastest
  const b = payload.route_healthy
  const t = payload.tradeoff
  return (
    <section className="panel">
      {t.same_route ? (
        <div className="samecard">
          <h3>Same route for both objectives</h3>
          <p>{a.minutes} minutes · {a.dose_ug} µg — no safer detour exists for this trip.</p>
        </div>
      ) : (
        <>
          <RouteCard title="Route A · fastest" minutes={a.minutes} dose={a.dose_ug} cls="card-a" via={a.via} />
          <RouteCard title="Route B · breathe-safe" minutes={b.minutes} dose={b.dose_ug} cls="card-b" via={b.via} />
        </>
      )}
    </section>
  )
}

function RouteCard({ title, minutes, dose, cls, via }: {
  title: string; minutes: number; dose: number; cls: string; via: string[]
}) {
  return (
    <div className={`card ${cls}`}>
      <div className="card-head">{title}</div>
      <div className="row">
        <span className="num">{minutes}</span><span className="unit">min</span>
        <span className="divider" />
        <span className="num">{dose}</span><span className="unit">µg inhaled</span>
      </div>
      <div className="via">{via.length ? via.join(' · ') : 'via the corridor grid'}</div>
    </div>
  )
}
