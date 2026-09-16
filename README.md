# SpillTrace AI

**From Oil Spill Detection to Intelligent Vessel Attribution**

SpillTrace AI is an AI-powered maritime forensic intelligence platform. It detects marine oil
spills from satellite imagery, reconstructs the probable origin of a spill using environmental
conditions and drift modelling, correlates the reconstructed origin with historical AIS vessel
trajectories, and ranks potential source vessels using explainable evidence.

> **DEMO DATA** — This foundation build runs entirely on realistic simulated data.
> Nothing shown in the UI is real-world evidence.

---

## Architecture

```text
SpillTrace AI/
├── backend/                  # FastAPI + SQLAlchemy (SQLite dev, PostGIS-ready)
│   ├── app/
│   │   ├── api/routes/       # Thin REST endpoints (/api/v1/*)
│   │   ├── core/             # Config, logging, security
│   │   ├── models/           # SQLAlchemy domain models (UUID PKs, GeoJSON fields)
│   │   ├── schemas/          # Pydantic request/response contracts
│   │   ├── services/         # Domain logic behind interfaces (mock + real slots)
│   │   ├── repositories/     # Persistence layer
│   │   ├── data/mock/        # Seed dataset (5 investigations, 15+ vessels, ...)
│   │   └── utils/            # Geo helpers
│   └── tests/
│
└── frontend/                 # React 19 + TypeScript + Vite + Tailwind 4 + MapLibre GL
    └── src/
        ├── app/              # Router, providers
        ├── components/       # ui/, layout/, map/, investigation/
        ├── features/         # dashboard, investigations, spills, map, vessels,
        │                     # drift, evidence, reports, data-sources, settings
        ├── services/api/     # Typed API client
        └── types/            # Shared domain types
```

### Design principles

- **Modular services behind interfaces** — `SpillDetector`, `DriftModel`, `AttributionEngine`,
  `CounterfactualSimulator`, `ReportGenerator` all have mock implementations selected via
  `USE_MOCK_MODELS`. Real implementations (U-Net/DeepLabV3+, OceanParcels, XGBoost) plug in
  without changing API contracts.
- **No business logic in routes** — routes call repositories/services only.
- **API versioning** — everything lives under `/api/v1`.
- **Scientific integrity** — the UI always speaks in terms of *attribution likelihood*,
  *candidate vessels* and *evidence strength*, never definitive blame.

---

## Quick start

### Backend (port 8000)

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

The SQLite database (`spilltrace.db`) is created and seeded automatically on startup.

- API docs (Swagger): http://127.0.0.1:8000/api/v1/docs
- ReDoc: http://127.0.0.1:8000/api/v1/redoc

### Frontend (port 5173)

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — Vite proxies `/api/*` to the backend on port 8000.

---

## Environment variables

See `backend/.env.example`. Key settings:

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./spilltrace.db` | Swap for `postgresql://...` (PostGIS) in production |
| `USE_MOCK_MODELS` | `True` | `False` requires real model implementations |
| `BACKEND_CORS_ORIGINS` | localhost list | Allowed frontend origins |
| `SENTINEL_API_KEY` / `SPIRE_AIS_API_KEY` | empty | Reserved for real data adapters |

Frontend: set `VITE_API_URL` to override the default `/api/v1` base (uses the dev proxy).

---

## API surface (v1)

```text
GET  /api/v1/dashboard
GET  /api/v1/investigations            POST /api/v1/investigations
GET  /api/v1/investigations/{id}       GET  /api/v1/investigations/{id}/spills
GET  /api/v1/investigations/{id}/drift GET  /api/v1/investigations/{id}/attribution
GET  /api/v1/investigations/{id}/evidence
GET  /api/v1/investigations/{id}/report
GET  /api/v1/spills                    POST /api/v1/spills/detect
GET  /api/v1/vessels                   GET  /api/v1/vessels/{id}/trajectory
POST /api/v1/drift/simulate            GET  /api/v1/drift/{id}
POST /api/v1/attribution/analyze
GET  /api/v1/evidence                  GET  /api/v1/data-sources
POST /api/v1/reports
```

---

## Future integration points

| Area | Interface | Planned implementation |
|---|---|---|
| SAR ingestion | `data/adapters/` | Sentinel-1 via Copernicus Data Space |
| Spill segmentation | `SpillDetector` | PyTorch U-Net / DeepLabV3+ |
| Drift modelling | `DriftModel` | OceanParcels Lagrangian simulation |
| Origin estimation | `OriginEstimator` | Probabilistic backward plume |
| AIS feed | `data/adapters/` | Spire / historical AIS store |
| Attribution | `AttributionEngine` | Multi-evidence model (XGBoost + rules) |
| Counterfactual | `CounterfactualSimulator` | Per-vessel forward drift simulation |
| Persistence | repositories | PostgreSQL + PostGIS spatial queries |
| Reports | `ReportGenerator` | PDF rendering service |
| Auth | `core/security.py` | JWT / OAuth2 |

---

## Testing

```powershell
cd backend
pytest tests/ -v
```

Frontend type-check + build:

```powershell
cd frontend
npm run build
```
