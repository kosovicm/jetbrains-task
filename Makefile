ifneq (,$(wildcard .env))
	include .env
	export $(shell sed 's/=.*//' .env)
else
	$(error .env file not found.)
endif

GRAFANA_URL = http://localhost:3000
DOCKER_FILE = docker-compose.yml 
DASHBOARD_DIR = ./monitoring/grafana/dashboards

.PHONY: all build up down clean dashboard dashboard-auto check

all: up

# Interactive dashboard (asks the user for metrics)
dashboard:
	@echo "Generating Grafana dashboard JSON (interactive)..."
	@python3 generate_dashboard.py

# CI/CD dashboard (without asking, uses METRICS and optionally NAME)
dashboard-auto:
ifndef METRICS
	$(error METRICS variable not set. Example: make dashboard-auto METRICS="cpu,memory")
endif
	@echo "Generating Grafana dashboard for CI/CD..."
	@METRICS="$(METRICS)" NAME="$(NAME)" python3 generate_dashboard.py

build:
	@echo "Building environment..."
	@docker compose -f $(DOCKER_FILE) build

up: dashboard
	@echo "Starting environment..."
	@docker compose -f $(DOCKER_FILE) up -d

down:
	@echo "Stopping containers..."
	@docker compose -f $(DOCKER_FILE) down

clean:
	@echo "Removing all containers and volumes..."
	@docker compose -f $(DOCKER_FILE) down -v

check:
	@echo "Checking Grafana provisioning..."
	@docker exec grafana ls /etc/grafana/provisioning/dashboards || echo "error: dashboards.yml missing"
	@docker exec grafana ls /var/lib/grafana/dashboards || echo "error: dashboard JSON missing"
