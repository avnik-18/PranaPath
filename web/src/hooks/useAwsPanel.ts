import { useCallback, useEffect, useState } from 'react'
import { fetchAwsPanel } from '../lib/api'
import type { AwsPanelData } from '../types'

export interface AwsRuntime {
  panel: AwsPanelData | null
  busy: boolean
  error: string
  reload: () => void
}

export function useAwsPanel(): AwsRuntime {
  const [panel, setPanel] = useState<AwsPanelData | null>(null)
  const [busy, setBusy] = useState(true)
  const [error, setError] = useState('')

  const load = useCallback(() => {
    setBusy(true)
    setError('')
    fetchAwsPanel()
      .then((r) => {
        if (r.ok) setPanel(r.data)
        else throw new Error('aws panel not ok')
      })
      .catch((e: unknown) => setError(String(e)))
      .finally(() => setBusy(false))
  }, [])

  useEffect(() => { load() }, [load])

  return { panel, busy, error, reload: load }
}
