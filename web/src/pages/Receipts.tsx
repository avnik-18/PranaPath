import { useAwsPanel } from '../hooks/useAwsPanel'
import { AwsPanel } from '../components/aws/AwsPanel'

type Props = { onBack: () => void }

export function Receipts(p: Props) {
  const rt = useAwsPanel()
  if (rt.busy) return <div className="loading">reading the ops ledger…</div>
  if (rt.error) return (
    <div className="ops">
      <div className="banner-err">ops console failed: {rt.error} <button className="ghost" onClick={rt.reload}>retry</button></div>
    </div>
  )
  if (!rt.panel) return <div className="loading">no panel</div>
  return <AwsPanel data={rt.panel} onBack={p.onBack} />
}
