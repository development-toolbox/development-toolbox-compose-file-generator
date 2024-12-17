#!/usr/bin/env python3

import subprocess
import sys

def start_test_container():
    try:
        # Run a test container for the purpose of testing the script (Grafana in this case)
        print("Starting test container (Grafana)...")
        subprocess.run([
            "docker", "run", "--name", "test-grafana", "-d",
            "--publish", "3000:3000", "--env", "GF_SECURITY_ADMIN_PASSWORD=admin",
            "--env", "GF_INSTALL_PLUGINS=grafana-piechart-panel",
            "grafana/grafana"
        ], check=True)
        print("Test container (Grafana) started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Could not start the container. {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_test_container()
