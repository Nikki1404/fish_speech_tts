.PHONY: download start stop logs client smoke

download:
	./scripts/download_model.sh

start:
	./scripts/start.sh

stop:
	docker compose down

logs:
	docker compose logs -f

client:
	python client/ws_client.py

smoke:
	python tests/smoke_test.py
