/* The ONLY bridge to the outside world (fixture bundle or the API). Nothing else fetches. */
import type { AwsPanelPayload, RoutesPayload } from '../types'

const FIXTURE = import.meta.env.VITE_FIXTURE !== 'false'
const BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? ''

export async function fetchPanel(trip: string, mode: string, budget: string): Promise<RoutesPayload> {
  const suffix = budget === 'any' ? '' : `-b${budget}`
  if (FIXTURE || !BASE) {
    const r = await fetch(new URL(`fixture-${trip}-${mode}${suffix}.json`, window.location.href))
    if (!r.ok) throw new Error(`fixture-${trip}-${mode}${suffix} unavailable (${r.status})`)
    return (await r.json()) as RoutesPayload
  }
  const url = `${BASE}/routes?trip=${encodeURIComponent(trip)}&mode=${mode}&budget=${encodeURIComponent(budget)}`
  const r = await fetch(url)
  if (!r.ok) throw new Error(`api ${r.status}`)
  return (await r.json()) as RoutesPayload
}

export async function fetchAwsPanel(): Promise<AwsPanelPayload> {
  if (FIXTURE || !BASE) {
    const r = await fetch(new URL('fixture-aws-panel.json', window.location.href))
    if (!r.ok) throw new Error(`aws fixture unavailable (${r.status})`)
    return (await r.json()) as AwsPanelPayload
  }
  const r = await fetch(`${BASE}/aws/panel`)
  if (!r.ok) throw new Error(`aws api ${r.status}`)
  return (await r.json()) as AwsPanelPayload
}
