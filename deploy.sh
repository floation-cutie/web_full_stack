#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_NAME="goodservices"
BACKUP_DIR="./backups"
COMPOSE_FILE="docker-compose.yml"

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Checking requirements..."

    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi

    log_info "All requirements satisfied"
}

backup_database() {
    log_info "Creating database backup..."

    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/goodservices_$(date +%Y%m%d_%H%M%S).sql"

    if ! docker-compose exec -T mysql mysqladmin ping -h localhost -u root -p"${MYSQL_ROOT_PASSWORD:-rootpassword123}" &> /dev/null; then
        log_error "MySQL is not running"
        return 1
    fi

    docker-compose exec -T mysql mysqldump -u root -p"${MYSQL_ROOT_PASSWORD:-rootpassword123}" "${MYSQL_DATABASE:-goodservices}" > "$BACKUP_FILE"

    log_info "Database backed up to: $BACKUP_FILE"
}

deploy_development() {
    log_info "Deploying to DEVELOPMENT environment..."

    if [ ! -f .env ]; then
        log_warn ".env file not found, copying from .env.example"
        cp .env.example .env
    fi

    log_info "Building and starting services..."
    docker-compose -f "$COMPOSE_FILE" build
    docker-compose -f "$COMPOSE_FILE" up -d

    log_info "Waiting for services to be ready..."
    sleep 15

    log_info "Development deployment complete!"
    log_info "Frontend: http://localhost:80"
    log_info "Backend API: http://localhost:8000"
    log_info "API Docs: http://localhost:8000/docs"
}

deploy_production() {
    log_info "Deploying to PRODUCTION environment..."

    if [ ! -f .env ]; then
        log_error ".env file not found! Please create it from .env.example"
        exit 1
    fi

    backup_database

    log_info "Building and starting services..."
    docker-compose -f "$COMPOSE_FILE" build
    docker-compose -f "$COMPOSE_FILE" up -d

    log_info "Waiting for services to be ready..."
    sleep 15

    log_info "Production deployment complete!"
}

stop_services() {
    log_info "Stopping all services..."
    docker-compose down
    log_info "Services stopped"
}

restart_services() {
    log_info "Restarting all services..."
    docker-compose restart
    log_info "Services restarted"
}

view_logs() {
    SERVICE=${1:-}
    if [ -z "$SERVICE" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f "$SERVICE"
    fi
}

health_check() {
    log_info "Performing health check..."

    if docker-compose exec mysql mysqladmin ping -h localhost -u root -p"${MYSQL_ROOT_PASSWORD:-rootpassword123}" &> /dev/null; then
        log_info "MySQL: ${GREEN}healthy${NC}"
    else
        log_error "MySQL: ${RED}unhealthy${NC}"
    fi

    if wget --quiet --tries=1 -O /dev/null http://localhost:8000/health &> /dev/null; then
        log_info "Backend: ${GREEN}healthy${NC}"
    else
        log_error "Backend: ${RED}unhealthy${NC}"
    fi

    if wget --quiet --tries=1 -O /dev/null http://localhost/ &> /dev/null; then
        log_info "Frontend: ${GREEN}healthy${NC}"
    else
        log_error "Frontend: ${RED}unhealthy${NC}"
    fi
}

status_services() {
    log_info "Service status:"
    docker-compose ps
}

case "$1" in
    dev)
        check_requirements
        deploy_development
        ;;
    prod)
        check_requirements
        deploy_production
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        view_logs "$2"
        ;;
    backup)
        backup_database
        ;;
    health)
        health_check
        ;;
    status)
        status_services
        ;;
    *)
        echo "Usage: $0 {dev|prod|stop|restart|logs [service]|backup|health|status}"
        echo ""
        echo "Commands:"
        echo "  dev      - Deploy to development environment"
        echo "  prod     - Deploy to production environment"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  logs     - View logs (optional: specify service)"
        echo "  backup   - Backup database"
        echo "  health   - Check service health"
        echo "  status   - Show service status"
        exit 1
        ;;
esac
