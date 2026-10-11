import type { RoutesPayload } from '../types'

export function ExplanationCard({ payload }: { payload: RoutesPayload }) {
  const ex = payload.explanation
  return (
    <section className="panel">
      <blockquote className="quote">“{ex.sentence}”</blockquote>
      <div className="srcrow">
        <span className={`pill ${ex.source === 'bedrock' ? 'pill-ai' : 'pill-soft'}`}>
          {ex.source === 'bedrock' ? 'explained by Bedrock' : 'engine template'}
        </span>
        {ex.validated && <span className="pill pill-ok">validator-passed</span>}
      </div>
    </section>
  )
}
