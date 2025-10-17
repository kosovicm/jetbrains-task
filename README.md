# Grafana Dashboard Generator — Internship Project

This project automates the creation of Grafana dashboards with Docker, Python, and Makefile orchestration. It supports both **interactive manual usage** and **CI/CD automated workflows**, demonstrating best practices in scripting, environment management, and reproducible deployments.

---

## Key Contributions

- **docker-compose.yml** — Defines the containerized environment (Grafana, Prometheus).  
- **generate_dashboard.py** — Python script to generate Grafana dashboard JSON dynamically.  
  - Supports **interactive prompts** or non-interactive **CI/CD mode** via environment variables (`METRICS` and optional `NAME`).  
  - **Built-in metrics**:  
    - CPU Usage (%)  
    - Memory Usage (MB)  
    - Disk Usage (%)  
    - Network Traffic (bytes/s)  
  - Ensures unique filenames to prevent overwriting or allows custom filenames via `NAME`.  
- **Makefile** — Orchestrates dashboard generation, Docker Compose operations, and CI/CD targets:  
  - `dashboard` — interactive mode  
  - `dashboard-auto` — automated CI/CD mode for pipelines  
  - `build`, `up`, `down`, `clean`, `check` — container lifecycle management  

---

---

## Usage Instructions

### 1. Interactive (manual)

Run the interactive generator — the script will ask which metrics to include:

```bash
make dashboard

### 2. Automated / CI/CD Mode

Use this in CI pipelines or scripts (no interactive prompts). Provide required `METRICS` and optional `NAME`:

```bash
make dashboard-auto METRICS="cpu,memory,disk" NAME="ci_dashboard_2025_10_17"
