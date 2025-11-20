DB_NAME = d33tcode
DB_DIR = db
BACKEND_DIR = backend

.PHONY: db-create db-seed db-fix-passwords db-reset run-backend

db-create:
	psql -d $(DB_NAME) -f $(DB_DIR)/schema.sql

db-seed:
	psql -d $(DB_NAME) -f $(DB_DIR)/seed_example_db.sql

db-fix-passwords:
	cd $(BACKEND_DIR) && uv run python fix_passwords.py

db-reset: db-drop db-create db-seed db-fix-passwords

db-drop:
	- dropdb $(DB_NAME) || true
	createdb $(DB_NAME)

run-backend:
	cd $(BACKEND_DIR) && uv run uvicorn main:app --reload