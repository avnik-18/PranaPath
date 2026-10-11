import type { AwsInventoryRow } from '../../types'

type Props = { inventory: AwsInventoryRow[] }

export function AwsServiceCard(p: Props) {
  return (
    <div className="aws-grid">
      {p.inventory.map((row) => {
        const live = row.status.includes('(live)')
        return (
          <div className={`aws-svccard ${live ? 'is-live' : 'is-mock'}`} key={row.service}>
            <div className="aws-svc-top">
              <span className={`svc-dot ${live ? 'ok' : ''}`} />
              <b>{row.service}</b>
            </div>
            <div className="aws-svc-role">{row.role}</div>
            <div className="aws-svc-status">{row.status} · {row.group}</div>
          </div>
        )
      })}
    </div>
  )
}
