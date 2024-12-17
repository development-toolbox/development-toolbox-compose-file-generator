# **development-toolbox-compose-file-generator**  

**A Python tool to generate `docker-compose.yml` or `podman-compose.yml` files from existing running containers.**  

---

## **Key Features**  
- Supports **Docker Compose** and **Podman Compose**.  
- Captures container configurations:  
  - Image  
  - Ports  
  - Environment Variables  
  - Volumes  
  - Networks  
- Generates clean, reusable Compose files.  
- Simplifies recreating multi-container environments.  

---

## **Prerequisites**  

Before using this tool, ensure you have:  
- **Python 3.x**  
- **Docker** or **Podman** installed and running  
- At least one running container  

---

## **Installation**  

Clone the repository and install the dependencies:  

```bash
git clone https://github.com/development-toolbox/development-toolbox-compose-file-generator
cd development-toolbox-compose-file-generator
pip3 install -r requirements.txt
```

---

## **Usage**  

### **Syntax**  

```bash
python3 compose-file-generator.py <container_name> <output_file>
```

- `<container_name>`: Name of the running container.  
- `<output_file>`: Path for the generated Compose file (e.g., `docker-compose.yml`).  

---

## **Examples**  

### **1. Basic Container Inspection and Compose Generation**  

1. **Run a Docker container**:  

```bash
docker run --name mattermost-preview -d \
  --publish 8065:8065 --publish 8075:8075 \
  --env MATTERMOST_ENV=production \
  --env DATABASE_URL=postgres://db:5432 \
  docker.io/mattermost/mattermost-preview
```

2. **Generate a Compose file**:  

```bash
python3 compose-file-generator.py mattermost-preview docker-compose.yml
```

3. **Generated `docker-compose.yml`**:  

```yaml
services:
  mattermost-preview:
    container_name: mattermost-preview
    image: docker.io/mattermost/mattermost-preview
    ports:
      - 8065:8065
      - 8075:8075
    environment:
      MATTERMOST_ENV: production
      DATABASE_URL: postgres://db:5432
    networks:
      - default
```

---

### **2. Container with Custom Network**  

1. **Create a custom network**:  

```bash
docker network create custom-network
```

2. **Run the container on the network**:  

```bash
docker run --name mattermost-preview -d --network custom-network \
  --publish 8065:8065 --env MATTERMOST_ENV=production \
  --env DATABASE_URL=postgres://db:5432 \
  docker.io/mattermost/mattermost-preview
```

3. **Generate the Compose file**:  

```bash
python3 compose-file-generator.py mattermost-preview custom-network.yml
```

4. **Generated `custom-network.yml`**:  

```yaml

services:
  mattermost-preview:
    container_name: mattermost-preview
    image: docker.io/mattermost/mattermost-preview
    ports:
      - 8065:8065
    environment:
      MATTERMOST_ENV: production
      DATABASE_URL: postgres://db:5432
    networks:
      custom-network:
        driver: bridge

networks:
  custom-network:
    driver: bridge
```

---

### **3. Container with Volumes**  

1. **Run the container with volumes**:  

```bash
docker run --name mattermost-preview -d \
  --publish 8065:8065 \
  --mount type=bind,source=/local/data,destination=/app/data \
  --env MATTERMOST_ENV=production \
  --env DATABASE_URL=postgres://db:5432 \
  docker.io/mattermost/mattermost-preview
```

2. **Generate the Compose file**:  

```bash
python3 compose-file-generator.py mattermost-preview volume-compose.yml
```

3. **Generated `volume-compose.yml`**:  

```yaml

services:
  mattermost-preview:
    container_name: mattermost-preview
    image: docker.io/mattermost/mattermost-preview
    ports:
      - 8065:8065
    environment:
      MATTERMOST_ENV: production
      DATABASE_URL: postgres://db:5432
    volumes:
      - /local/data:/app/data
    networks:
      - default
```

---

## **Troubleshooting**  

| **Problem**                         | **Solution**                                    |  
|-------------------------------------|------------------------------------------------|  
| Script fails to detect container    | Ensure the container is running and named correctly. |  
| Permission errors                   | is docker or podman setup correctly test it with docker run hello-world or podman run hello-world
 |  
| Missing dependencies                | Install required dependencies: `pip3 install -r requirements.txt`. |  

---

## **License**  

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## **Author**  
**Johan Sörell**  
- [GitHub](https://github.com/J-SirL/)  
- [LinkedIn](https://se.linkedin.com/in/johansorell)  
- [Blog](insertmyblogname)  
