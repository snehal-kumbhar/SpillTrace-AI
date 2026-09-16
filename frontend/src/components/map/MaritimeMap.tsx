import { useEffect, useRef, useState } from 'react';
import { Map, NavigationControl, ScaleControl, type GeoJSONSource } from 'maplibre-gl';
import type { Feature, FeatureCollection } from 'geojson';
import type { DashboardMapData } from '../../types';
import { Layers, Maximize2, RotateCcw, ZoomIn, ZoomOut } from 'lucide-react';
import clsx from 'clsx';

export interface MapLayerVisibility {
  spills: boolean;
  origins: boolean;
  vessels: boolean;
  candidates: boolean;
  tracks: boolean;
  investigationBoundary: boolean;
}

const DEFAULT_LAYERS: MapLayerVisibility = {
  spills: true,
  origins: true,
  vessels: true,
  candidates: true,
  tracks: false,
  investigationBoundary: false,
};

interface MaritimeMapProps {
  mapData?: DashboardMapData;
  center?: [number, number];
  zoom?: number;
  className?: string;
  showControls?: boolean;
  showLayerControl?: boolean;
  showTimeline?: boolean;
  onVesselClick?: (vesselId: string) => void;
  trajectoryGeoJson?: FeatureCollection;
  driftGeoJson?: FeatureCollection;
  height?: string;
}

const LAYER_LABELS: Record<keyof MapLayerVisibility, string> = {
  spills: 'Oil Spill Detection',
  origins: 'Probable Origin',
  vessels: 'AIS Vessel Tracks',
  candidates: 'Candidate Vessels',
  tracks: 'Vessel Trajectories',
  investigationBoundary: 'Investigation Boundary',
};

function buildGeoJson(mapData: DashboardMapData) {
  const features: Feature[] = [];

  if (mapData.spills) {
    for (const spill of mapData.spills) {
      features.push({
        type: 'Feature',
        properties: {
          type: 'spill',
          id: spill.id,
          name: spill.name,
          area: spill.area_km2,
          status: spill.status,
        },
        geometry: {
          type: 'Polygon',
          coordinates: [spill.polygon_coordinates],
        },
      });
    }
  }

  if (mapData.origins) {
    for (const origin of mapData.origins) {
      features.push({
        type: 'Feature',
        properties: {
          type: 'origin',
          probability: origin.probability,
          uncertainty: origin.uncertainty_km,
        },
        geometry: {
          type: 'Point',
          coordinates: [origin.lon, origin.lat],
        },
      });
    }
  }

  if (mapData.vessels) {
    for (const v of mapData.vessels) {
      features.push({
        type: 'Feature',
        properties: {
          type: 'vessel',
          id: v.id,
          name: v.name,
          imo: v.imo,
          heading: v.heading,
          sog: v.sog_knots,
          is_candidate: v.is_candidate,
        },
        geometry: {
          type: 'Point',
          coordinates: [v.lon, v.lat],
        },
      });
    }
  }

  return { type: 'FeatureCollection' as const, features };
}

export function MaritimeMap({
  mapData,
  center = [67.0, 20.0],
  zoom = 5,
  className,
  showControls = true,
  showLayerControl = true,
  showTimeline = false,
  onVesselClick,
  trajectoryGeoJson,
  driftGeoJson,
  height = '100%',
}: MaritimeMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<Map | null>(null);
  const [layers, setLayers] = useState<MapLayerVisibility>(DEFAULT_LAYERS);
  const [layerPanelOpen, setLayerPanelOpen] = useState(false);
  const [timelineStep, setTimelineStep] = useState(4);
  const timelineHours = ['12:00', '14:00', '16:00', '18:00', '20:00'];

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = new Map({
      container: containerRef.current,
      style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
      center,
      zoom,
      attributionControl: false,
    });

    map.addControl(new NavigationControl({ showCompass: true }), 'top-right');
    map.addControl(new ScaleControl({ unit: 'metric' }), 'bottom-left');

    map.on('load', () => {
      map.addSource('maritime-data', {
        type: 'geojson',
        data: mapData ? buildGeoJson(mapData) : { type: 'FeatureCollection', features: [] },
      });

      map.addLayer({
        id: 'spill-fill',
        type: 'fill',
        source: 'maritime-data',
        filter: ['==', ['get', 'type'], 'spill'],
        paint: {
          'fill-color': '#f59e0b',
          'fill-opacity': 0.25,
        },
      });

      map.addLayer({
        id: 'spill-outline',
        type: 'line',
        source: 'maritime-data',
        filter: ['==', ['get', 'type'], 'spill'],
        paint: {
          'line-color': '#f59e0b',
          'line-width': 2,
          'line-opacity': 0.8,
        },
      });

      map.addLayer({
        id: 'origin-glow',
        type: 'circle',
        source: 'maritime-data',
        filter: ['==', ['get', 'type'], 'origin'],
        paint: {
          'circle-radius': 18,
          'circle-color': '#22d3ee',
          'circle-opacity': 0.15,
          'circle-blur': 0.8,
        },
      });

      map.addLayer({
        id: 'origin-point',
        type: 'circle',
        source: 'maritime-data',
        filter: ['==', ['get', 'type'], 'origin'],
        paint: {
          'circle-radius': 6,
          'circle-color': '#22d3ee',
          'circle-stroke-color': '#ffffff',
          'circle-stroke-width': 1.5,
        },
      });

      map.addLayer({
        id: 'vessel-point',
        type: 'circle',
        source: 'maritime-data',
        filter: ['all', ['==', ['get', 'type'], 'vessel'], ['==', ['get', 'is_candidate'], false]],
        paint: {
          'circle-radius': 5,
          'circle-color': '#64748b',
          'circle-stroke-color': '#94a3b8',
          'circle-stroke-width': 1,
        },
      });

      map.addLayer({
        id: 'candidate-vessel',
        type: 'circle',
        source: 'maritime-data',
        filter: ['all', ['==', ['get', 'type'], 'vessel'], ['==', ['get', 'is_candidate'], true]],
        paint: {
          'circle-radius': 7,
          'circle-color': '#ef4444',
          'circle-stroke-color': '#fca5a5',
          'circle-stroke-width': 2,
        },
      });

      if (trajectoryGeoJson) {
        map.addSource('trajectories', { type: 'geojson', data: trajectoryGeoJson });
        map.addLayer({
          id: 'trajectory-lines',
          type: 'line',
          source: 'trajectories',
          paint: { 'line-color': '#22d3ee', 'line-width': 2, 'line-opacity': 0.7 },
        });
      }

      if (driftGeoJson) {
        map.addSource('drift-data', { type: 'geojson', data: driftGeoJson });
        map.addLayer({
          id: 'drift-high',
          type: 'fill',
          source: 'drift-data',
          filter: ['==', ['get', 'zone'], 'high'],
          paint: { 'fill-color': '#22d3ee', 'fill-opacity': 0.3 },
        });
        map.addLayer({
          id: 'drift-medium',
          type: 'fill',
          source: 'drift-data',
          filter: ['==', ['get', 'zone'], 'medium'],
          paint: { 'fill-color': '#0891b2', 'fill-opacity': 0.15 },
        });
        map.addLayer({
          id: 'drift-low',
          type: 'fill',
          source: 'drift-data',
          filter: ['==', ['get', 'zone'], 'low'],
          paint: { 'fill-color': '#164e63', 'fill-opacity': 0.1 },
        });
        map.addLayer({
          id: 'drift-tracks',
          type: 'line',
          source: 'drift-data',
          filter: ['==', ['get', 'zone'], 'track'],
          paint: { 'line-color': '#67e8f9', 'line-width': 1, 'line-opacity': 0.4, 'line-dasharray': [2, 2] },
        });
      }
    });

    map.on('click', 'candidate-vessel', (e) => {
      const id = e.features?.[0]?.properties?.id;
      if (id && onVesselClick) onVesselClick(id);
    });
    map.on('click', 'vessel-point', (e) => {
      const id = e.features?.[0]?.properties?.id;
      if (id && onVesselClick) onVesselClick(id);
    });

    mapRef.current = map;
    return () => { map.remove(); mapRef.current = null; };
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || !mapData) return;
    const source = map.getSource('maritime-data') as GeoJSONSource | undefined;
    if (source) source.setData(buildGeoJson(mapData));
  }, [mapData]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map?.isStyleLoaded()) return;
    const setVis = (id: string, visible: boolean) => {
      if (map.getLayer(id)) map.setLayoutProperty(id, 'visibility', visible ? 'visible' : 'none');
    };
    setVis('spill-fill', layers.spills);
    setVis('spill-outline', layers.spills);
    setVis('origin-glow', layers.origins);
    setVis('origin-point', layers.origins);
    setVis('vessel-point', layers.vessels);
    setVis('candidate-vessel', layers.candidates);
    if (map.getLayer('trajectory-lines')) setVis('trajectory-lines', layers.tracks);
  }, [layers]);

  const toggleLayer = (key: keyof MapLayerVisibility) =>
    setLayers((prev) => ({ ...prev, [key]: !prev[key] }));

  return (
    <div className={clsx('relative', className)} style={{ height }}>
      <div ref={containerRef} className="absolute inset-0 rounded-sm overflow-hidden" />

      {showControls && (
        <div className="absolute top-3 left-3 flex flex-col gap-1 z-10">
          <MapButton icon={ZoomIn} onClick={() => mapRef.current?.zoomIn()} title="Zoom in" />
          <MapButton icon={ZoomOut} onClick={() => mapRef.current?.zoomOut()} title="Zoom out" />
          <MapButton icon={RotateCcw} onClick={() => mapRef.current?.flyTo({ center, zoom })} title="Reset view" />
          {showLayerControl && (
            <MapButton icon={Layers} onClick={() => setLayerPanelOpen(!layerPanelOpen)} title="Layers" active={layerPanelOpen} />
          )}
          <MapButton icon={Maximize2} onClick={() => containerRef.current?.requestFullscreen()} title="Fullscreen" />
        </div>
      )}

      {layerPanelOpen && (
        <div className="absolute top-3 left-14 z-10 bg-navy-900/95 border border-panel-border rounded-sm p-3 min-w-52 backdrop-blur-sm">
          <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-2">Map Layers</p>
          {(Object.keys(LAYER_LABELS) as Array<keyof MapLayerVisibility>).map((key) => (
            <label key={key} className="flex items-center gap-2 py-1 text-xs cursor-pointer hover:text-accent">
              <input
                type="checkbox"
                checked={layers[key]}
                onChange={() => toggleLayer(key)}
                className="accent-cyan-400"
              />
              {LAYER_LABELS[key]}
            </label>
          ))}
        </div>
      )}

      {showTimeline && (
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-10 bg-navy-900/95 border border-panel-border rounded-sm px-4 py-3 backdrop-blur-sm min-w-80">
          <p className="text-[10px] uppercase tracking-wider text-text-muted mb-2 text-center">Investigation Timeline</p>
          <div className="flex items-center justify-between gap-2">
            {timelineHours.map((h, i) => (
              <button
                key={h}
                type="button"
                onClick={() => setTimelineStep(i)}
                className={clsx(
                  'font-mono text-xs px-2 py-1 rounded transition-colors',
                  i <= timelineStep ? 'text-accent bg-accent/10' : 'text-text-muted',
                )}
              >
                {h}
              </button>
            ))}
          </div>
          <input
            type="range"
            min={0}
            max={4}
            value={timelineStep}
            onChange={(e) => setTimelineStep(Number(e.target.value))}
            className="w-full mt-2 accent-cyan-400"
          />
        </div>
      )}
    </div>
  );
}

function MapButton({ icon: Icon, onClick, title, active }: {
  icon: React.ComponentType<{ className?: string }>;
  onClick: () => void;
  title: string;
  active?: boolean;
}) {
  return (
    <button
      type="button"
      title={title}
      onClick={onClick}
      className={clsx(
        'w-8 h-8 flex items-center justify-center bg-navy-900/95 border border-panel-border rounded-sm text-text-muted hover:text-accent hover:border-accent/30 transition-colors',
        active && 'text-accent border-accent/40',
      )}
    >
      <Icon className="w-4 h-4" />
    </button>
  );
}

export function buildDriftGeoJson(drift: import('../../types').DriftSimulation): FeatureCollection {
  const features: Feature[] = [];
  const zones = drift.probability_zones;
  if (zones) {
    for (const [zone, coords] of Object.entries(zones) as Array<[string, number[][]]>) {
      features.push({
        type: 'Feature',
        properties: { zone },
        geometry: { type: 'Polygon', coordinates: [coords] },
      });
    }
  }
  if (drift.particle_tracks) {
    for (const track of drift.particle_tracks) {
      features.push({
        type: 'Feature',
        properties: { zone: 'track' },
        geometry: {
          type: 'LineString',
          coordinates: track.map((p) => [p.lon, p.lat]),
        },
      });
    }
  }
  features.push({
    type: 'Feature',
    properties: { zone: 'origin-point' },
    geometry: { type: 'Point', coordinates: [drift.origin_lon, drift.origin_lat] },
  });
  return { type: 'FeatureCollection', features };
}
