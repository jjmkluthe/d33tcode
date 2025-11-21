DB_NAME = d33tcode
DB_DIR = db
BACKEND_DIR = backend
FRONTEND_DIR = frontend

.PHONY: db-create db-seed db-fix-passwords db-reset run-backend build-frontend run-frontend run-all

db-create:
	psql -d $(DB_NAME) -f $(DB_DIR)/schema.sql

db-seed:
	psql -d $(DB_NAME) -f $(DB_DIR)/seed_example_db.sql

db-fix-passwords:
	cd $(BACKEND_DIR) && uv run python -m example_setup.example_user_passwords

db-reset: db-drop db-create db-seed db-fix-passwords

db-drop:
	- dropdb $(DB_NAME) || true
	createdb $(DB_NAME)

run-backend:
	cd $(BACKEND_DIR) && uv run uvicorn main:app --reload

build-frontend:
	cd $(FRONTEND_DIR) && npm install && npm run build

run-frontend:
	cd $(FRONTEND_DIR) && npm run dev

run-all:
	make run-backend &
	make run-frontend