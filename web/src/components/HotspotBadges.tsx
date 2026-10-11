import type { RoutesPayload } from '../types'

export function HotspotBadges({ payload }: { payload: RoutesPayload }) {
  const hs = payload.hotspots.fastest
  if (payload.tradeoff.same_route || hs.length === 0) return null
  return (
    <section className="panel">
      <h4>Avoided / causing the dose</h4>
      <div className="chips">
        {hs.map((h) => (
          <span className="chip" key={h.edge_id}>
            {h.edge_id} <span className="chip-sub">{h.pm25_ug_m3} µg/m³ · {h.share_pct}% of dose</span>
          </span>
        ))}
      </div>
    </section>
  )
}
