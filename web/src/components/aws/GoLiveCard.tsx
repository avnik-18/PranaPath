const STEPS = [
  { n: '1', t: "copy .env.example → .env and drop in the TEAM account keys",
    c: '.env' },
  { n: '2', t: 'rehearse, then run the deploy (receipts land in data/receipts)',
    c: 'wsl python3 infra/deploy.py --dry-run' },
  { n: '3', t: 'reload this console — the stamp flips MOCK → LIVE (probe-backed rows turn green)',
    c: 'reload' },
]

export function GoLiveCard() {
  return (
    <div className="aws-golive">
      <div className="aws-h">go live in 3 steps</div>
      {STEPS.map((s) => (
        <div className="golive-row" key={s.n}>
          <span className="golive-n">{s.n}</span>
          <span className="golive-t">{s.t}</span>
          <code>{s.c}</code>
        </div>
      ))}
    </div>
  )
}
