# Grafana Dashboard Generator

This project automates the creation of Grafana dashboards with Docker, Python, and Makefile orchestration. It supports both **interactive manual usage** and **CI/CD automated workflows**.

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
```
### 2. Automated / CI/CD Mode

Use this in CI pipelines or scripts (no interactive prompts). Provide required `METRICS` and optional `NAME`:
 - METRICS (required): comma-separated metric keys

 - NAME (optional): desired JSON filename; if omitted, a unique timestamped file is created

   This allows dashboards to be generated automatically in CI/CD pipelines without manual input

```bash
make dashboard-auto METRICS="cpu,memory,disk" NAME="ci_dashboard_2025_10_17"
```

### 3. Start/Stop/Clean Environment

  - make up
  - make down
  - make clean ( stop and removes volumes )

