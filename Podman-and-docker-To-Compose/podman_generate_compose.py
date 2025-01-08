import subprocess
import yaml
import sys

def get_container_details(container_name):
    try:
        # Kör `podman inspect` och hämta information om containern
        result = subprocess.run(["podman", "inspect", container_name], capture_output=True, text=True, check=True)
        return yaml.safe_load(result.stdout)[0]
    except subprocess.CalledProcessError as e:
        print(f"Fel: Kunde inte inspektera containern {container_name}. Kontrollera namnet.")
        sys.exit(1)

def convert_to_compose(container_data):
    # Hämta grundläggande information
    image = container_data.get("Config", {}).get("Image", "unknown")
    ports = container_data.get("NetworkSettings", {}).get("Ports", {})
    container_name = container_data.get("Name", "").lstrip("/")  # Ta bort '/' från namnet

    # Bygg compose-strukturen
    compose = {
        "version": "3.9",
        "services": {
            container_name: {
                "image": image,
                "container_name": container_name,
                "ports": [],
            }
        }
    }

    # Lägg till portbindningar från NetworkSettings
    if ports:
        for container_port, host_ports in ports.items():
            if host_ports:  # Kontrollera att host_ports inte är None
                for binding in host_ports:
                    host_port = binding.get("HostPort")
                    if host_port:
                        compose["services"][container_name]["ports"].append(f"{host_port}:{container_port.split('/')[0]}")

    return compose

def save_to_yaml(compose_data, output_file):
    try:
        with open(output_file, "w") as file:
            yaml.dump(compose_data, file, default_flow_style=False)
        print(f"Compose-fil sparad som: {output_file}")
    except Exception as e:
        print(f"Fel: Kunde inte spara compose-filen. {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Användning: python3 generate_compose.py <container_name> <output_file>")
        sys.exit(1)

    container_name = sys.argv[1]
    output_file = sys.argv[2]

    container_data = get_container_details(container_name)
    compose_data = convert_to_compose(container_data)
    save_to_yaml(compose_data, output_file)
