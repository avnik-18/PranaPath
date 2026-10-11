import type { AwsActivity } from '../../types'

type Props = { activities: AwsActivity[] }

export function AwsEventFeed(p: Props) {
  return (
    <div className="aws-feed">
      {p.activities.map((a, i) => (
        <div className="aws-feedrow" key={i}>
          <span className="feed-ts">{a.ts}</span>
          <span className={`feed-svc ${a.mock ? 'mock' : 'live'}`}>{a.service}</span>
          <span className="feed-ev"><b>{a.event}</b> — {a.detail}</span>
        </div>
      ))}
    </div>
  )
}
