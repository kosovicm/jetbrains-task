import json
import os
from pathlib import Path

# Define available metrics and their corresponding Prometheus expressions
AVAILABLE_METRICS = {
    "cpu": {
        "title": "CPU Usage (%)",
        "expr": 'rate(process_cpu_seconds_total{job="petclinic"}[1m]) * 100',
        "unit": "percent"
    },
    "memory": {
        "title": "Memory Usage (MB)",
        "expr": '(process_resident_memory_bytes{job="petclinic"}) / 1024 / 1024',
        "unit": "megabytes"
    },
    "disk": {
        "title": "Disk Usage (%)",
        "expr": '(node_filesystem_size_bytes{job="petclinic"} - node_filesystem_free_bytes{job="petclinic"}) / node_filesystem_size_bytes{job="petclinic"} * 100',
        "unit": "percent"
    },
    "network": {
        "title": "Network Traffic (bytes/s)",
        "expr": 'rate(node_network_receive_bytes_total{job="petclinic"}[1m]) + rate(node_network_transmit_bytes_total{job="petclinic"}[1m])',
        "unit": "bytes"
    }
}
# Asking user which metrics want to monitor
def ask_metrics():
    print("=== Select metrics to monitor ===")
    print("Available options: ", ", ".join(AVAILABLE_METRICS.keys()))
    chosen = input("Enter desired metrics (comma-separated, e.g., cpu,memory): ").strip().lower()
    selected = [m.strip() for m in chosen.split(",") if m.strip() in AVAILABLE_METRICS]
    
    if not selected:
        print("No valid metrics selected. Defaulting to CPU")
        selected = ["cpu"]
    return selected


def generate_dashboard(metrics, output_path="./monitoring/grafana/dashboards/custom_dashboard.json"):
    panels = []
    y_offset = 0

    for i, m in enumerate(metrics, start=1):
        data = AVAILABLE_METRICS[m]
        panel = {
            "type": "timeseries",
            "title": data["title"],
            "id": i,
            "gridPos": {"h": 8, "w": 24, "x": 0, "y": y_offset},
            "targets": [{"expr": data["expr"], "refId": "A"}],
            "fieldConfig": {"defaults": {"unit": data["unit"], "decimals": 2}, "overrides": []},
            "options": {
                "legend": {"displayMode": "list", "placement": "bottom"},
                "tooltip": {"mode": "single"}
            }
        }
        panels.append(panel)
        y_offset += 8  # move panels vertically

    dashboard = {
        "id": None,
        "uid": "custom-dashboard",
        "title": "Custom Monitoring Dashboard",
        "tags": ["observability", "prometheus"],
        "timezone": "browser",
        "schemaVersion": 37,
        "version": 1,
        "refresh": "10s",
        "panels": panels,
        "templating": {"list": []},
        "time": {"from": "now-1h", "to": "now"}
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)
    print(f"\n Grafana dashboard generated: {output_path}")


if __name__ == "__main__":
    # If the environment variable METRICS is defined, use it (automatic mode)
    metrics_env = os.getenv("METRICS")
    if metrics_env:
        selected_metrics = [m.strip() for m in metrics_env.split(",") if m.strip() in AVAILABLE_METRICS]
        if not selected_metrics:
            print("No valid metrics in METRICS variable. Defaulting to CPU.")
            selected_metrics = ["cpu"]
    else:
        # If not defined, ask the user interactively
        selected_metrics = ask_metrics()

    generate_dashboard(selected_metrics)
