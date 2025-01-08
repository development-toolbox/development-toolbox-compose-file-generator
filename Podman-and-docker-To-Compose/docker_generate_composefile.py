import subprocess
import yaml
import sys

def get_container_details(container_name):
    try:
        # Run `docker inspect` and get the container details
        result = subprocess.run(["docker", "inspect", container_name], capture_output=True, text=True, check=True)
        return yaml.safe_load(result.stdout)[0]
    except subprocess.CalledProcessError as e:
        print(f"Error: Could not inspect container {container_name}. Check the container name.")
        sys.exit(1)

def convert_to_compose(container_data):
    # Get basic information
    image = container_data.get("Config", {}).get("Image", "unknown")
    ports = container_data.get("NetworkSettings", {}).get("Ports", {})
    container_name = container_data.get("Name", "").lstrip("/")  # Remove '/' from the name

    # Build the compose structure
    compose = {
        "services": {
            container_name: {
                "image": image,
                "container_name": container_name,
                "ports": [],
            }
        }
    }

    # Add port bindings from NetworkSettings
    if ports:
        for container_port, host_ports in ports.items():
            if host_ports:  # Check that host_ports is not None
                for binding in host_ports:
                    host_port = binding.get("HostPort")
                    if host_port:
                        compose["services"][container_name]["ports"].append(f"{host_port}:{container_port.split('/')[0]}")

    return compose

def save_to_yaml(compose_data, output_file):
    try:
        with open(output_file, "w") as file:
            yaml.dump(compose_data, file, default_flow_style=False)
        print(f"Compose file saved as: {output_file}")
    except Exception as e:
        print(f"Error: Could not save compose file. {e}")
        sys.exit(1)

def stop_remove_container(container_name):
    # Stop the container if it's running
    subprocess.run(["docker", "stop", container_name], capture_output=True, text=True)
    # Remove the container
    subprocess.run(["docker", "rm", container_name], capture_output=True, text=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 docker_generate_composefile.py <container_name> <output_file>")
        sys.exit(1)

    container_name = sys.argv[1]
    output_file = sys.argv[2]

    container_data = get_container_details(container_name)
    compose_data = convert_to_compose(container_data)
    save_to_yaml(compose_data, output_file)

    # Stop and remove the container before starting with Docker Compose
    stop_remove_container(container_name)

    # Start the container with Docker Compose
    subprocess.run(["docker-compose", "up", "-d"], capture_output=True, text=True)
