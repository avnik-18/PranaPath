/* Contract mirror of backend/api/schemas.py — additive only (see web/CLAUDE.md). */

export interface PathNode {
  id: string
  name: string
  lat: number
  lon: number
}

export interface RouteShape {
  route_id: string
  path: string[]
  via: string[]
  minutes: number
  km: number
  dose_ug: number
}

export interface SmogCell {
  polygon: [number, number][]
  core: [number, number][]
  pm25: number
  level: 'low' | 'mid' | 'high'
}

export interface Hotspot {
  edge_id: string
  pm25_ug_m3: number
  minutes: number
  share_pct: number
}

export interface Tradeoff {
  time_extra_minutes: number
  dose_saving_pct: number
  same_route: boolean
}

export interface Explanation {
  sentence: string
  source: 'template' | 'bedrock'
  validated: boolean
}

export interface RoutesPayload {
  ok: boolean
  api_version: string
  mode: string
  route_fastest: RouteShape
  route_healthy: RouteShape
  tradeoff: Tradeoff
  hotspots: { fastest: Hotspot[]; healthy: Hotspot[] }
  explanation: Explanation
  ui: { map_nodes: PathNode[]; smog: SmogCell[] }
}

/* ---- AWS ops panel (mirror of backend/api/aws_schemas.py v1) — additive ---- */

export interface AwsProbe {
  dynamodb_ok: boolean | null
  lambda_ok: boolean | null
  bedrock_ok: boolean | null
}

export interface AwsInventoryRow {
  service: string
  role: string
  group: string
  status: string
}

export interface AwsActivity {
  ts: string
  service: string
  event: string
  detail: string
  mock: boolean
}

export interface AwsReceipt {
  ts?: string
  kind: string
  payload: Record<string, unknown>
  mock?: boolean
}

export interface AwsCounts {
  services: number
  green_live: number
  green_mock: number
  events: number
  receipts: number
}

export interface AwsTrip {
  origin: string
  dest: string
  mode: string
}

export interface AwsPanelData {
  switch: 'mock' | 'live'
  mode: string
  region: string
  probe: AwsProbe
  reason: string
  inventory: AwsInventoryRow[]
  activities: AwsActivity[]
  receipts: AwsReceipt[]
  counts: AwsCounts
  trip: AwsTrip
  trip_minutes?: number
  dose_fastest_ug?: number
  dose_breathe_safe_ug?: number
}

export interface AwsPanelPayload {
  ok: boolean
  api_version: string
  data: AwsPanelData
}
