# Finance Dashboard API

Production-grade backend system built with FastAPI demonstrating clean architecture, RBAC, and containerized deployment.

## Architecture

```
app/
├── api/v1/          # Route handlers (thin controllers)
├── core/            # Config & database setup
├── models/          # SQLAlchemy ORM models
├── schemas/         # Pydantic validation schemas
├── repositories/    # Database access layer
├── services/        # Business logic layer
├── middleware/       # RBAC enforcement
├── utils/           # Logging utilities
└── exceptions/      # Custom exception classes
```

### Layered Design
- **API Layer**: Thin routes that delegate to services. No business logic.
- **Service Layer**: Business rules, validation orchestration, authorization checks.
- **Repository Layer**: All database operations isolated here. Easy to swap ORMs or databases.

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| **FastAPI** | Async-ready, auto-docs (OpenAPI), Pydantic integration, high performance |
| **Repository Pattern** | Decouples DB access from business logic; testable, swappable |
| **Header-based RBAC** | Simple demo of role enforcement; JWT recommended for production |
| **SQLite default** | Zero-config dev setup; switch to PostgreSQL via `DATABASE_URL` |
| **Custom AppException** | Consistent error format across the entire API |

## RBAC System

Roles: `viewer` < `analyst` < `admin`

| Endpoint | viewer | analyst | admin |
|----------|--------|---------|-------|
| GET /users | ✅ | ✅ | ✅ |
| POST /users | ❌ | ❌ | ✅* |
| GET /records | ✅ | ✅ | ✅ |
| POST/PUT/DELETE /records | ❌ | ❌ | ✅ |
| GET /dashboard/summary | ❌ | ✅ | ✅ |

*First user (bootstrap) can be created without headers.

Headers: `X-User-Id` (int), `X-User-Role` (viewer|analyst|admin)

> ⚠️ **Production note**: Replace header-based RBAC with JWT token validation. Headers can be spoofed.

## Quick Start

### Local
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker
```bash
docker build -t finance-api .
docker run -p 8000:8000 finance-api
```

### Docker Compose (preferred)
```bash
docker-compose up --build
```

Visit: http://localhost:8000/docs

## API Endpoints

### Users
- `POST /users` — Create user (bootstrap or admin-only)
- `GET /users` — List all users (viewer+)
- `PATCH /users/{id}` — Update user (admin)

### Financial Records
- `POST /records` — Create record (admin, user_id from headers)
- `GET /records` — List with filters & pagination (viewer+)
- `GET /records/{id}` — Get single record (viewer+)
- `PUT /records/{id}` — Update record (admin)
- `DELETE /records/{id}` — Delete record (admin)

### Dashboard
- `GET /dashboard/summary` — Aggregated financial summary (analyst+)

## Performance

- SQL `SUM`, `GROUP BY` for aggregations (no Python loops)
- Pagination via `skip`/`limit` query params
- Database indexes on `date`, `category`, `type`, `user_id`, `email`

## Error Handling

All errors return:
```json
{"success": false, "error": "message"}
```

No raw `HTTPException` — all errors flow through `AppException` → global handler.

## Future Improvements

- JWT authentication with refresh tokens
- Rate limiting middleware
- Redis caching for dashboard
- Cursor-based pagination
- Alembic migrations
- PostgreSQL `date_trunc` for monthly trends
- CI/CD pipeline
- Unit & integration test suite
# finance-dashboard-api
