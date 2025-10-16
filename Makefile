.PHONY: all build up down clean dashboard check

all: up

dashboard:
	@echo "🧠 Generating Grafana dashboard JSON..."
	python3 generate_cpu_dashboard.py

build:
	@echo "🐳 Building environment..."
	docker compose build

up: dashboard
	@echo "🚀 Starting environment..."
	docker compose up -d
	@echo "📊 Grafana → http://localhost:3000 (admin/admin)"

down:
	@echo "🛑 Stopping containers..."
	docker compose down

clean:
	@echo "🧹 Removing all containers and volumes..."
	docker compose down -v

check:
	@echo "🔍 Checking Grafana provisioning..."
	docker exec grafana ls /etc/grafana/provisioning/dashboards || echo "❌ dashboards.yml missing"
	docker exec grafana ls /var/lib/grafana/dashboards || echo "❌ dashboard JSON missing"
