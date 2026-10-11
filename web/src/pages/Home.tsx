import 'maplibre-gl/dist/maplibre-gl.css'
import { useRoutesRuntime } from '../hooks/useRoutesRuntime'
import { MapView } from '../components/MapView'
import { RoutePanel } from '../components/RoutePanel'
import { DoseCompare } from '../components/DoseCompare'
import { HotspotBadges } from '../components/HotspotBadges'
import { ExplanationCard } from '../components/ExplanationCard'

type Props = { onOpenReceipts: () => void }

const TRIPS = [
  { key: 'short', label: 'short · 3.1 km' },
  { key: 'medium', label: 'medium · 4.0 km' },
  { key: 'long', label: 'long · 5.7 km' },
]

const BUDGETS = [
  { key: 'any', label: 'no cap' },
  { key: '1.05', label: '≤ 1.05× fast' },
  { key: '1.1', label: '≤ 1.1× fast' },
]

export default function Home(p: Props) {
  const rt = useRoutesRuntime('short', 'jog', 'any')
  const payload = rt.payload

  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <span className="logo-dot" />
          <b>EcoRoute AI</b>
          <span className="tag">breathe-safe routing · Delhi</span>
        </div>
        <div className="tools">
          <label>
            trip
            <select value={rt.trip} onChange={(e) => rt.setTrip(e.target.value)}>
              {TRIPS.map((t) => <option key={t.key} value={t.key}>{t.label}</option>)}
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
          {rt.fixture && <span className="pill pill-soft">demo bundle</span>}
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
