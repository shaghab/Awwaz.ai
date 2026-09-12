# Awwaz

**Existing systems collect complaints. Awwaz works on what happens next.**

Awwaz is an AI civic agent that turns natural-language complaints (English, Urdu, Roman Urdu) into persistent, auditable workflows and keeps working on the next required action: understanding, structuring, routing, tracking responsibility, detecting stalled cases, recommending follow-up or escalation, and executing approved actions through a replaceable civic-service adapter.

Awwaz is not a replacement for existing complaint portals. It is the operational layer around a complaint after submission.

## Quick start

Prerequisites: Docker (for Postgres), [uv](https://docs.astral.sh/uv/), [pnpm](https://pnpm.io/), Python 3.11+, Node 22+.

```bash
cp .env.example .env          # placeholders are fine for local development
make install                  # backend (uv) + frontend (pnpm) dependencies
make dev                      # Postgres, migrations, seed, API on :8000, UI on :3000
```

Open http://localhost:3000, pick a demo persona on `/login`, and you are signed in. No passwords — demo sessions are enabled by `AWWAZ_DEMO_MODE=true` and return 404 when it is off.

| Persona | Role | Sees |
|---|---|---|
| Hamza Iqbal | `CITIZEN` | Report, My Complaints |
| Sara Khan | `OPERATOR` | Overview, Cases, Approvals, Recurring Issues, Activity |
| Bilal Ahmed | `ADMIN` | Configuration, Users, Audit |

### Common tasks

```bash
make check      # ruff, mypy, pytest, eslint, tsc, vitest, next build
make test       # both test suites
make migrate    # alembic upgrade head
make seed       # idempotent demo seed
make reset      # rebuild the schema from migrations, then seed
make help       # everything else
```

Backend tests create and drop their own PostgreSQL database. Point them at a
different server with `TEST_DATABASE_URL`.

## Layout

```text
backend/     FastAPI + SQLAlchemy + Alembic (modular monolith)
frontend/    Next.js App Router + TypeScript + Tailwind + TanStack Query
database/    seed configuration (YAML, from slice 2)
docs/slices/ the PRD broken into implementation slices
```

Every response carries `meta.request_id` (or `error.request_id`), every error uses
the canonical envelope, and every consequential action is written to `audit_logs`.

## Documents

- [`Awwaz_Full_PRD.md`](Awwaz_Full_PRD.md) — full implementation-ready product requirements (hackathon MVP v1.0).
- [`docs/slices/README.md`](docs/slices/README.md) — the PRD broken into six implementation slices, with the decision log and acceptance mapping.

## Implementation slices

| # | Slice | Status |
|---|-------|--------|
| 1 | [Foundation](docs/slices/01-foundation.md) | Done |
| 2 | [Complaint domain & operator surface](docs/slices/02-complaint-domain-and-operator-surface.md) | Not started |
| 3 | [Agent intake](docs/slices/03-agent-intake.md) | Not started |
| 4 | [Stall → Recommend → Approve → Act](docs/slices/04-stall-recommend-approve-act.md) | Not started |
| 5 | [Commitments, memory & recurrence](docs/slices/05-commitments-memory-recurrence.md) | Not started |
| 6 | [Evidence, notifications, hardening & demo](docs/slices/06-evidence-notifications-hardening-demo.md) | Not started |

## Stack

Next.js + TypeScript frontend, FastAPI + Python backend, PostgreSQL, a lightweight scheduled worker (slice 4), Anthropic Claude for language understanding (slice 3), and a mock civic-service adapter behind a replaceable interface (slice 4).
