const RINGS = [
  'data · JSON + keyless fetch',
  'engine · pure stdlib maths',
  'guardian · the caged agent',
  'api · thin glue only',
  'web · frontend island',
  'infra · nothing imports it',
]

const AWS: { group: string; chips: string[] }[] = [
  { group: 'front', chips: ['Amplify'] },
  { group: 'edge', chips: ['API Gateway', 'Lambda[engine]', 'Lambda[explainer]', 'Bedrock Nova Lite'] },
  { group: 'data', chips: ['DynamoDB'] },
  { group: 'health × advisory', chips: ['EventBridge 15-min', 'Lambda[aqi-refresh]', 'EventBridge 06:00', 'Step Functions', 'SNS'] },
  { group: 'ops', chips: ['CloudWatch', 'X-Ray', 'IAM', 'Powertools for AWS'] },
]

export function SystemRings() {
  return (
    <section className="sys" id="system">
      <div className="sec-kicker">THE SYSTEM</div>
      <h2>Six rings offline. <em>Fourteen AWS services</em> going live.</h2>
      <div className="sys-rings">
        {RINGS.map((r, i) => (
          <div className="ring" key={r}>
            <span className="ring-n">{i + 1}</span>{r}
          </div>
        ))}
      </div>
      <p className="sys-note">
        Engine numbers never cross Bedrock as free prose — Bedrock receives computed
        stats only and must repeat them back; the validator enforces it.
        Free tier only, region <b>ap-south-1</b> — no RDS / EC2 / NAT anywhere.
      </p>
      <div className="sys-aws">
        {AWS.map((g) => (
          <div className="aws-group" key={g.group}>
            <div className="aws-lbl">{g.group}</div>
            <div className="aws-chips">
              {g.chips.map((c) => <span className="aws-chip" key={c}>{c}</span>)}
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
