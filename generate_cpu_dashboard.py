import json
from pathlib import Path

def generate_cpu_dashboard(output_path="./monitoring/grafana/dashboards/cpu_dashboard.json"):
    dashboard = {
        "id": None,
        "uid": "cpu-usage-dashboard",
        "title": "CPU Usage Dashboard",
        "tags": ["observability", "cpu", "prometheus"],
        "timezone": "browser",
        "schemaVersion": 37,
        "version": 1,
        "refresh": "10s",
        "panels": [
            {
                "type": "timeseries",
                "title": "CPU Usage (%)",
                "id": 1,
                "gridPos": {"h": 8, "w": 24, "x": 0, "y": 0},
                "targets": [
                    {
                        "expr": 'rate(process_cpu_seconds_total{job="petclinic"}[1m]) * 100',
                        "refId": "A"
                    }
                ],
                "fieldConfig": {
                    "defaults": {"unit": "percent", "decimals": 2},
                    "overrides": []
                },
                "options": {
                    "legend": {"displayMode": "list", "placement": "bottom"},
                    "tooltip": {"mode": "single"}
                }
            }
        ],
        "templating": {
            "list": [
            ]
        },
        "time": {"from": "now-1h", "to": "now"}
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)
    print(f"Grafana dashboard saved to: {output_path}")


if __name__ == "__main__":
    generate_cpu_dashboard()
