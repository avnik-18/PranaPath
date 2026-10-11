const TECH = [
  'OpenStreetMap data', 'MapLibre GL', 'Dijkstra ×2', 'dose math',
  'validator-gated AI', 'AWS Bedrock', 'DynamoDB', 'EventBridge',
  'Step Functions', 'SNS', 'CloudWatch', 'X-Ray', 'Amplify',
]

export function Marquee() {
  return (
    <div className="marquee" aria-label="technology used">
      <div className="marquee-track">
        {[...TECH, ...TECH].map((t, i) => (
          <span className="marquee-item" key={i}>{t}</span>
        ))}
      </div>
    </div>
  )
}
