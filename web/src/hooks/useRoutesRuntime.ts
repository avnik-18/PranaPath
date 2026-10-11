/* Owns runtime data state; components receive plain typed objects. */
import { useCallback, useEffect, useState } from 'react'
import { fetchPanel } from '../lib/api'
import type { RoutesPayload } from '../types'

export type RuntimeState = {
  payload: RoutesPayload | null
  busy: boolean
  error: string | null
  fixture: boolean
  city: string
  trip: string
  mode: string
  budget: string
  setCity: (city: string) => void
  setTrip: (trip: string) => void
  setMode: (mode: string) => void
  setBudget: (budget: string) => void
  reload: () => void
}

const FIXTURE = import.meta.env.VITE_FIXTURE !== 'false'

export function useRoutesRuntime(initialCity: string, initialTrip: string, initialMode: string, initialBudget: string): RuntimeState {
  const [payload, setPayload] = useState<RoutesPayload | null>(null)
  const [busy, setBusy] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [city, setCity] = useState(initialCity)
  const [trip, setTrip] = useState(initialTrip)
  const [mode, setMode] = useState(initialMode)
  const [budget, setBudget] = useState(initialBudget)
  const [tick, setTick] = useState(0)

  useEffect(() => {
    let alive = true
    setBusy(true)
    setError(null)
    fetchPanel(city, trip, mode, budget)
      .then((p) => { if (alive) { setPayload(p); setBusy(false) } })
      .catch((e: unknown) => { if (alive) { setError(String(e)); setBusy(false) } })
    return () => { alive = false }
  }, [city, trip, mode, budget, tick])

  const reload = useCallback(() => setTick((t) => t + 1), [])

  return { payload, busy, error, fixture: FIXTURE, city, trip, mode, budget, setCity, setTrip, setMode, setBudget, reload }
}
