import 'maplibre-gl/dist/maplibre-gl.css'
import { useRoutesRuntime } from '../hooks/useRoutesRuntime'
import { MapView } from '../components/MapView'
import { RoutePanel } from '../components/RoutePanel'
import { DoseCompare } from '../components/DoseCompare'
import { HotspotBadges } from '../components/HotspotBadges'
import { ExplanationCard } from '../components/ExplanationCard'

type Props = { onOpenReceipts: () => void }

const CITIES = [
  { key: 'delhi', label: 'Delhi' },
  { key: 'blr', label: 'Bengaluru' },
]

const TRIPS: Record<string, { key: string; label: string }[]> = {
  delhi: [
    { key: 'short', label: 'short · 3.1 km' },
    { key: 'medium', label: 'medium · 4.0 km' },
    { key: 'long', label: 'long · 5.7 km' },
  ],
  blr: [
    { key: 'short', label: 'Koramangala · 4.8 km' },
    { key: 'medium', label: 'Indiranagar · 4.8 km' },
    { key: 'long', label: 'Jayanagar · 4.5 km' },
  ],
}

const BUDGETS = [
  { key: 'any', label: 'no cap' },
  { key: '1.05', label: '≤ 1.05× fast' },
  { key: '1.1', label: '≤ 1.1× fast' },
  { key: '1.35', label: '≤ 1.35× fast' },
  { key: '1.5', label: '≤ 1.5× fast' },
  { key: '2.0', label: '≤ 2× fast' },
]

export default function Home(p: Props) {
  const rt = useRoutesRuntime('delhi', 'short', 'jog', 'any')
  const payload = rt.payload
  const tripRows = TRIPS[rt.city] ?? TRIPS.delhi

  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <span className="logo-dot" />
          <b>PranaPath</b>
          <span className="tag">breathe-safe routing · India</span>
        </div>
        <div className="tools">
          <label>
            city
            <select value={rt.city} onChange={(e) => { rt.setCity(e.target.value); rt.setTrip('short') }}>
              {CITIES.map((c) => <option key={c.key} value={c.key}>{c.label}</option>)}
            </select>
          </label>
          <label>
            trip
            <select value={rt.trip} onChange={(e) => rt.setTrip(e.target.value)}>
              {tripRows.map((t) => <option key={t.key} value={t.key}>{t.label}</option>)}
            </select>
          </label>
          <label>
            cap
            <select value={rt.budget} onChange={(e) => rt.setBudget(e.target.value)}>
              {BUDGETS.map((b) => <option key={b.key} value={b.key}>{b.label}</option>)}
            </select>
          </label>
          {rt.budget !== 'any' && payload?.ok && (
            <span className="pill pill-ok">route within {rt.budget}× fast ✓</span>
          )}
          {rt.fixture && <span className="pill pill-soft">local engine</span>}
          <button className="ghost" onClick={p.onOpenReceipts}>receipts</button>
          <button className="ghost" onClick={rt.reload}>reload</button>
        </div>
      </header>

      {rt.error && <div className="banner-err">{rt.error}</div>}

      <main className="split">
        <section className="mapwrap"><MapView payload={payload} /></section>
        <aside className="side">
          {payload && payload.ok && (
            <>
              <RoutePanel payload={payload} />
              <DoseCompare payload={payload} />
              <HotspotBadges payload={payload} />
              <ExplanationCard payload={payload} />
            </>
          )}
          {rt.busy && <div className="loading">computing doses…</div>}
        </aside>
      </main>

      <footer className="foot">
        every number here comes from the engine (C × IR × minutes, per segment) — the AI only words it. · {new Date().getFullYear()}
      </footer>
    </div>
  )
}
