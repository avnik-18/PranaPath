import { useEffect, useRef } from 'react'
import maplibregl from 'maplibre-gl'
import type { RoutesPayload } from '../types'

export function MapView({ payload }: { payload: RoutesPayload | null }) {
  const box = useRef<HTMLDivElement>(null)
  const map = useRef<maplibregl.Map | null>(null)

  useEffect(() => {
    if (map.current || !box.current) return
    map.current = new maplibregl.Map({
      container: box.current,
      style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
      center: [77.12, 28.715],
      zoom: 12.2,
      preserveDrawingBuffer: true,
      fadeDuration: 0,
    })
    map.current.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right')
    ;(window as unknown as { __ecorouteMap?: maplibregl.Map }).__ecorouteMap = map.current
  }, [])

  useEffect(() => {
    const m = map.current
    if (!m || !payload || !payload.ok) return

    const paint = () => {
      const nodePos = new Map(payload.ui.map_nodes.map((n) => [n.id, { lat: n.lat, lon: n.lon }]))

    const line = (path: string[]) => {
      const pts = path.map((id) => nodePos.get(id)).filter(Boolean)
        .map((v) => [v!.lon, v!.lat])
      return { type: 'Feature' as const, properties: {}, geometry: { type: 'LineString' as const, coordinates: pts } }
    }

    const hotspots = payload.hotspots.fastest.map((h) => {
      const [u, v] = h.edge_id.split('-')
      const a = nodePos.get(u), b = nodePos.get(v)
      return a && b
        ? {
            edge_id: h.edge_id,
            pm25: h.pm25_ug_m3,
            mid: [(a.lon + b.lon) / 2, (a.lat + b.lat) / 2],
          }
        : null
    }).filter(Boolean)

    if (!m.getSource('routes')) m.addSource('routes', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } })
    ;(m.getSource('routes') as maplibregl.GeoJSONSource).setData(toFC([line(payload.route_fastest.path), line(payload.route_healthy.path)]))
    if (!m.getSource('smog')) m.addSource('smog', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } })
    if (!m.getSource('puffs')) m.addSource('puffs', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } })
    ;(m.getSource('smog') as maplibregl.GeoJSONSource).setData(toFC(payload.ui.smog.map((c) => ({
      type: 'Feature' as const,
      properties: { pm25: c.pm25, level: c.level },
      geometry: { type: 'Polygon' as const, coordinates: [c.polygon] },
    }))))
    ;(m.getSource('puffs') as maplibregl.GeoJSONSource).setData(toFC(payload.ui.puffs.map((p) => ({
      type: 'Feature' as const,
      properties: { pm25: p.pm25, level: p.level },
      geometry: { type: 'Polygon' as const, coordinates: [p.polygon] },
    }))))
    if (!m.getSource('hotspots')) m.addSource('hotspots', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } })
    ;(m.getSource('hotspots') as maplibregl.GeoJSONSource).setData(toFC(hotspots.map((h) => ({
      type: 'Feature' as const,
      properties: { pm25: String(h!.pm25) },
      geometry: { type: 'Point' as const, coordinates: h!.mid },
    }))))

      if (!m.getLayer('lineB')) {
        m.addLayer({
          id: 'smogfill', type: 'fill', source: 'smog',
          paint: {
            'fill-color': ['match', ['get', 'level'],
              'high', '#ff5a2d', 'mid', '#b06a4a', '#57646f'],
            'fill-opacity': 0.3,
          },
        })
        m.addLayer({
          id: 'smogcore', type: 'fill', source: 'smog',
          paint: {
            'fill-color': ['match', ['get', 'level'],
              'high', '#ff7a4d', 'mid', '#c97b52', '#64717c'],
            'fill-opacity': 0.42,
          },
        })
        m.addLayer({
          id: 'pufffill', type: 'fill', source: 'puffs',
          paint: {
            'fill-color': ['match', ['get', 'level'],
              'high', '#ffa659', 'mid', '#e0854f', '#7b8592'],
            'fill-opacity': 0.6,
          },
        }, 'smogcore')
        m.addLayer({ id: 'lineB', type: 'line', source: 'routes', filter: ['==', ['get', 'route'], 'B'],
          layout: { 'line-cap': 'round', 'line-join': 'round' },
          paint: { 'line-color': '#4fc3ff', 'line-width': 6.5, 'line-opacity': 0.92 } }, 'smogcore')
        m.addLayer({ id: 'lineA', type: 'line', source: 'routes', filter: ['==', ['get', 'route'], 'A'],
          layout: { 'line-cap': 'round', 'line-join': 'round' },
          paint: { 'line-color': '#ff6a3d', 'line-width': 3.5, 'line-opacity': 0.98, 'line-dasharray': [1.4, 1.3] } }, 'lineB')
        m.addLayer({ id: 'hotdot', type: 'circle', source: 'hotspots',
          paint: { 'circle-radius': 9, 'circle-color': '#ffdd55', 'circle-stroke-color': '#ff6a3d', 'circle-stroke-width': 2.5 } }, 'lineA')
        m.fitBounds(bounds(nodePos), { padding: 70, duration: 400 })
      }
    }

    if (m.isStyleLoaded()) paint()
    else m.once('load', paint)
  }, [payload])

  /* route tag: unzip into two features below (sorted by draw order) */
  function toFC(features: GeoJSON.Feature[]): GeoJSON.FeatureCollection {
    const tagged = features.map((f, i) => ({ ...f, properties: { route: i === 0 ? 'A' : 'B' } }))
    return { type: 'FeatureCollection', features: tagged }
  }

  function bounds(nodePos: Map<string, { lat: number; lon: number }>) {
    const lats = [...nodePos.values()].map((v) => v.lat)
    const lons = [...nodePos.values()].map((v) => v.lon)
    return [[Math.min(...lons), Math.min(...lats)], [Math.max(...lons), Math.max(...lats)]] as [[number, number], [number, number]]
  }

  return <div className="map" ref={box} aria-label="route map" />
}
