import 'maplibre-gl/dist/maplibre-gl.css'
import { useRoutesRuntime } from '../hooks/useRoutesRuntime'
import { MapView } from '../components/MapView'
import { RoutePanel } from '../components/RoutePanel'
import { DoseCompare } from '../components/DoseCompare'
import { HotspotBadges } from '../components/HotspotBadges'
import { ExplanationCard } from '../components/ExplanationCard'

type Props = { onOpenReceipts: () => void }

export default function Home(p: Props) {
  const rt = useRoutesRuntime('ashok_vihar', 'model_town', 'jog')
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
            mode
            <select value={rt.mode} onChange={(e) => rt.setMode(e.target.value)} disabled={rt.fixture}>
              <option value="jog">jog</option>
              <option value="cycle">cycle</option>
              <option value="walk">walk</option>
            </select>
          </label>
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
