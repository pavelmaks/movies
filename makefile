up:
	docker compose up

down:
	docker compose down -v

remove:
	docker image rm new_admin_panel_sprint_3-service

local_db:
	docker compose up db

etl:
	docker compose up db etl elastic

admin:
	docker-compose exec service python manage.py createsuperuser