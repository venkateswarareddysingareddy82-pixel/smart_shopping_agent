# Seed data
`products.json` is an export of the demo catalogue (105 fictional products). The database is seeded automatically from `backend/app/seed_data.py` when the backend starts with an empty database.
Re-export after editing: `cd backend && python -m app.seed --export`. Recreate: `python -m app.seed --reset`.
