import type { AwsPanelData } from '../../types'
import { AwsEventFeed } from './AwsEventFeed'
import { EnvChecklist } from './EnvChecklist'
import { GoLiveCard } from './GoLiveCard'

type Props = { data: AwsPanelData; onBack: () => void }

export function AwsPanel(p: Props) {
  const d = p.data
  return (
    <div className="ops">
      <header className="ops-head">
        <div className="brand">
          <span className="logo-dot" />
          <b>PranaPath</b>
          <span className="tag">ops console</span>
        </div>
        <div className="ops-state">
          <span className={`ops-stamp ${d.switch === 'live' ? 'live' : 'mock'}`}>
            {d.switch === 'live' ? 'LIVE' : 'MOCK'} · {d.region}
          </span>
          <button className="ghost" onClick={p.onBack}>← back to app</button>
        </div>
      </header>

      {d.switch === 'mock' && (
        <div className="ops-banner">
          MOCK VIEW — every row below is deterministic and traceable to the real trip
          (<b>{d.trip.origin} → {d.trip.dest} · {d.trip.mode} · fastest {d.trip_minutes} min ·
          {' '}{d.dose_fastest_ug} µg vs {d.dose_breathe_safe_ug} µg</b>).
          Drop the team keys into <code>.env</code> and this stamp flips LIVE with zero code change — {d.reason ? '' : 'see the 3-step card.'}
        </div>
      )}
      {d.switch === 'live' && (
        <div className="ops-banner live">
          LIVE — probed against region {d.region}. {d.reason}
        </div>
      )}

      <div className="ops-counts">{d.counts.services} services · {d.counts.green_live} live-verified · {d.counts.events} events · {d.counts.receipts} receipts</div>
      <div className="ops-stack">{d.inventory.map((i) => i.service).join(' · ')}</div>

      <div className="ops-duo">
        <div className="ops-col">
          <div className="aws-h">activity feed {d.switch === 'mock' && '(mock)'}</div>
          <AwsEventFeed activities={d.activities} />
        </div>
        <div className="ops-col">
          <EnvChecklist probe={d.probe} />
          <GoLiveCard />
        </div>
      </div>
    </div>
  )
}
