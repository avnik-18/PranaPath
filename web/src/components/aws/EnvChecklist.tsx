import type { AwsProbe } from '../../types'

type Props = { probe: AwsProbe }

export function EnvChecklist(p: Props) {
  const live = p.probe.dynamodb_ok !== null || p.probe.lambda_ok !== null || p.probe.bedrock_ok !== null
  const rows = [
    { name: 'AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY', ok: live },
    { name: 'AWS_REGION=ap-south-1', ok: true },
    { name: 'DynamoDB probe (route table)', ok: p.probe.dynamodb_ok },
    { name: 'Lambda probe (engine + explainer + aqi)', ok: p.probe.lambda_ok },
    { name: 'Bedrock probe (Nova Lite invoke)', ok: p.probe.bedrock_ok },
  ]
  return (
    <div className="aws-check">
      <div className="aws-h">env checklist</div>
      {rows.map((r) => (
        <div className="check-row" key={r.name}>
          <span className={`check-mark ${r.ok ? 'ok' : 'todo'}`}>{r.ok ? '✓' : '○'}</span>
          <span>{r.name}</span>
        </div>
      ))}
    </div>
  )
}
