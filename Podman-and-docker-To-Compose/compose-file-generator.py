import subprocess
import yaml
import sys

def get_container_details(container_name):
    try:
        # Run `docker inspect` to get container details
        result = subprocess.run(["docker", "inspect", container_name], capture_output=True, text=True, check=True)
        return yaml.safe_load(result.stdout)[0]
    except subprocess.CalledProcessError as e:
        print(f"Error: Could not inspect the container {container_name}. Ensure the container is running and check the name.")
        sys.exit(1)

def convert_to_compose(container_data):
    # Get the basic information
    image = container_data.get("Config", {}).get("Image", "unknown")
    ports = container_data.get("NetworkSettings", {}).get("Ports", {})
    container_name = container_data.get("Name", "").lstrip("/")  # Remove '/' from the name
    environment = container_data.get("Config", {}).get("Env", [])
    volumes = container_data.get("Mounts", [])

    # Start building the compose structure
    compose = {
        "services": {
            container_name: {
                "image": image,
                "container_name": container_name,
                "ports": [],
                "environment": {},
                "volumes": []
            }
        }
    }

    # Add port bindings from NetworkSettings
    if ports:
        for container_port, host_ports in ports.items():
            if host_ports:
                for binding in host_ports:
                    host_port = binding.get("HostPort")
                    if host_port:
                        compose["services"][container_name]["ports"].append(f"{host_port}:{container_port.split('/')[0]}")

    # Add environment variables
    if environment:
        for env in environment:
            key, value = env.split("=", 1)
            compose["services"][container_name]["environment"][key] = value

    # Add volumes if any
    if volumes:
        for mount in volumes:
            if mount.get("Destination"):
                compose["services"][container_name]["volumes"].append(f"{mount['Source']}:{mount['Destination']}")

    return compose

def save_to_yaml(compose_data, output_file):
    try:
        with open(output_file, "w") as file:
            yaml.dump(compose_data, file, default_flow_style=False)
        print(f"Compose file saved as: {output_file}")
    except Exception as e:
        print(f"Error: Could not save the compose file. {e}")
        sys.exit(1)

def remove_container(container_name):
    try:
        # Remove the running container
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True, text=True, check=True)
        print(f"Container {container_name} has been removed.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Could not remove container {container_name}.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 compose-file-generator.py <container_name> <output_file>")
        sys.exit(1)

    container_name = sys.argv[1]
    output_file = sys.argv[2]

    container_data = get_container_details(container_name)
    compose_data = convert_to_compose(container_data)
    save_to_yaml(compose_data, output_file)
    
    # After generating the compose file, remove the container
    remove_container(container_name)