#!/usr/bin/env python3

import subprocess
import os
import pytest

def run_docker_compose_test():
    try:
        # Run the compose file generation script with the test container
        print("Running the compose generator script for the test container...")
        result = subprocess.run(
            ["python3", "../compose-file-generator.py", "test-grafana", "test-docker-compose.yml"],
            capture_output=True, text=True, check=True
        )
        assert "Compose file saved as" in result.stdout
        print("Compose file generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Could not generate the compose file. {e}")
        pytest.fail(f"Test failed with error: {e}")

def cleanup():
    # Cleanup by removing the test container
    subprocess.run(["docker", "rm", "-f", "test-grafana"], capture_output=True, text=True, check=True)

@pytest.fixture(scope="module", autouse=True)
def container_cleanup():
    # Ensure that the test container is cleaned up after the test
    yield
    cleanup()

if __name__ == "__main__":
    run_docker_compose_test()
