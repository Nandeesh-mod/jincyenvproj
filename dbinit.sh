#!/bin/bash

# MySQL docker Management Script

# Configuration Variables
MYSQL_CONTAINER_NAME="wastemanage-mysql"
MYSQL_ROOT_PASSWORD="jincy123"
MYSQL_DATABASE="wastemanage"
MYSQL_USER="jincy"
MYSQL_PASSWORD="jincy123"
MYSQL_PORT=3306
MYSQL_DATA_VOLUME="./data"

# Create a data folder in the current directory

# Function to start MySQL container
start_mysql() {
    echo "Starting MySQL container..."
    docker run -d \
        --name ${MYSQL_CONTAINER_NAME} \
        -e MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD} \
        -e MYSQL_DATABASE=${MYSQL_DATABASE} \
        -e MYSQL_USER=${MYSQL_USER} \
        -e MYSQL_PASSWORD=${MYSQL_PASSWORD} \
        -p ${MYSQL_PORT}:3306 \
        -v ${MYSQL_DATA_VOLUME}:/var/lib/mysql \
        docker.io/mysql:latest
}

# Function to stop MySQL container
stop_mysql() {
    echo "Stopping MySQL container..."
    docker stop ${MYSQL_CONTAINER_NAME}
    docker rm ${MYSQL_CONTAINER_NAME}
}

# Function to check container status
status_mysql() {
    docker ps -f name=${MYSQL_CONTAINER_NAME}
}

# Function to view logs
logs_mysql() {
    docker logs ${MYSQL_CONTAINER_NAME}
}

# Function to connect to MySQL shell
connect_mysql() {
    docker exec -it ${MYSQL_CONTAINER_NAME} mysql -u ${MYSQL_USER} -p${MYSQL_PASSWORD}
}

remove_container() {
    docker stop ${MYSQL_CONTAINER_NAME} && docker rm ${MYSQL_CONTAINER_NAME}
}

# Main script logic
case "$1" in 
    start)
        start_mysql
        ;;
    stop)
        stop_mysql
        ;;
    restart)
        stop_mysql
        start_mysql
        ;;
    status)
        status_mysql
        ;;
    logs)
        logs_mysql
        ;;
    connect)
        connect_mysql
        ;;
    remove)
        remove_container
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|connect}"
        exit 1
esac

exit 0