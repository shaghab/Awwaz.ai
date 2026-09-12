# Seed configuration

Departments, routing rules, the escalation chain, and stall thresholds live in the
database, seeded from YAML in this folder (D10). Nothing category-related is
hard-coded in a prompt.

Slice 1 seeds users only, from `backend/app/domain/users/service.py`. The YAML
fixtures arrive with slice 2.
