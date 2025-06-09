#!/bin/bash
set -e

source .env

# Display usage information
show_usage() {
  echo "Usage: $0 [OPTION]"
  echo "Options:"
  echo "  start    Start the User Service with Docker Compose"
  echo "  stop     Stop the User Service"
  echo "  restart  Restart the User Service"
  echo "  logs     Show logs from the User Service"
  echo "  status   Check the status of the User Service containers"
  echo "  clean    Stop and remove containers, networks, and volumes"
  echo "  help     Display this help message"
}

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
  echo "docker-compose is not installed. Please install it first."
  exit 1
fi

# Process command line arguments
case "$1" in
  start)
    echo "Starting User Service..."
    docker-compose up -d
    echo "User Service started successfully"
    echo "API documentation is available at http://localhost:${PORT}/ui"
    ;;
  stop)
    echo "Stopping User Service..."
    docker-compose stop
    echo "User Service stopped"
    ;;
  restart)
    echo "Restarting User Service..."
    docker-compose restart
    echo "User Service restarted"
    ;;
  logs)
    echo "Showing logs from User Service..."
    docker-compose logs -f
    ;;
  status)
    echo "User Service status:"
    docker-compose ps
    ;;
  clean)
    echo "Cleaning up User Service containers, networks, and volumes..."
    docker-compose down -v
    docker images backend-app -q | xargs -r docker rmi
    echo "Cleanup complete"
    ;;
  help|*)
    show_usage
    ;;
esac
