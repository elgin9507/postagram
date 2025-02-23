# Postagram Service

This repository contains Postagram API.

## Prerequisites

- Docker
- Docker Compose

## Quickstart

Run API and all of dependencies:

```bash
make dev
```

API is now hosted at: http://localhost:8080/

View API docs at: http://localhost:8080/docs

## Usage

### Build the Docker Image

```bash
make build
```

This command builds the Docker image for the web service.

### Start the Service

```bash
make up
```

This command starts the Docker service in detached mode.

### Build and Start the Service

```bash
make buildup
```

This command combines the build and up commands to build the Docker image and start the service.

### Stop the Service

```bash
make down
```

This command stops all Docker containers.

### View Logs

```bash
make logs
```

This command displays the logs of the Docker containers.

### Open Shell

```bash
make shell
```

This command opens a shell inside the Docker container.

### Create Database Migrations

```bash
make makemigrations <message>
```

This command creates database migration with the provided message.

### Run Database Migrations

```bash
make migrate
```

This command runs database migrations.

## Directory Structure

- `postagram`: Contains the source code for Postagram.
- `Dockerfile`: Dockerfile for Postagram API image.
- `docker-compose.yml`: Docker Compose configuration file.
- `Makefile`: Makefile for managing Docker commands and database migrations.


### Source Code Structure

- `postagram/models`: Model layer - contains definitions for database models
- `postragram/domain`: Services layer - contains all business logic
- `postagram/controllers`: Controller layer - contains implementation of API endpoints
- `postagram/db` - Abstractions for initializing/accessing database
- `postagram/schemas` - Request/Reponse schemas for API
- `postagram/settings.py` - Application settings - contains all configurable things
- `postagram/main.py` - Entrypoint of the application
