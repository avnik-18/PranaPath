/* Owns runtime data state; components receive plain typed objects. */
import { useCallback, useEffect, useState } from 'react'
import { fetchPanel } from '../lib/api'
import type { RoutesPayload } from '../types'

export type RuntimeState = {
  payload: RoutesPayload | null
  busy: boolean
  error: string | null
  fixture: boolean
  origin: string
  dest: string
  mode: string
  setTrip: (origin: string, dest: string) => void
  setMode: (mode: string) => void
  reload: () => void
}

const FIXTURE = import.meta.env.VITE_FIXTURE !== 'false'

export function useRoutesRuntime(initialOrigin: string, initialDest: string, initialMode: string): RuntimeState {
  const [payload, setPayload] = useState<RoutesPayload | null>(null)
  const [busy, setBusy] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [origin, setOrigin] = useState(initialOrigin)
  const [dest, setDest] = useState(initialDest)
  const [mode, setModeState] = useState(initialMode)
  const [tick, setTick] = useState(0)

  useEffect(() => {
    let alive = true
    setBusy(true)
    setError(null)
    fetchPanel(origin, dest, mode)
      .then((p) => { if (alive) { setPayload(p); setBusy(false) } })
      .catch((e: unknown) => { if (alive) { setError(String(e)); setBusy(false) } })
    return () => { alive = false }
  }, [origin, dest, mode, tick])

  const setTrip = useCallback((o: string, d: string) => { setOrigin(o); setDest(d) }, [])
  const setMode = useCallback((m: string) => setModeState(m), [])
  const reload = useCallback(() => setTick((t) => t + 1), [])

  return { payload, busy, error, fixture: FIXTURE, origin, dest, mode, setTrip, setMode, reload }
}
