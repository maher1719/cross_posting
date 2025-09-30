#!/bin/bash
#
# project.sh - Helper scripts for the Cross-Posting App
#
# Usage:
#   source ./project.sh
#   Then you can use the functions like 'dcup', 'dcdown', etc.
#

# Base command
dc() {
    docker compose "$@"
}

# Start everything up
dcup() {
    dc up -d --build
}

# Stop everything
dcdown() {
    dc down
}

# Nuke everything (including volumes)
dcnuke() {
    dc down -v
}

# Restart everything
dcrestart() {
    echo "--- Restarting all containers ---"
    dcdown && dcup
}

# Rebuild and restart everything
dcreb() {
    echo "--- Rebuilding and restarting all containers ---"
    dcdown && dc up -d --build
}


# View the logs of all services, streaming in real-time.
dclog() {
    dc logs -f 
}



# View the logs of a specific service (e.g., dclog worker).
# Note: This is a function to allow passing an argument.
dclog() {
    dc logs -f "$1"
}



# Execute a command inside a running container.
# e.g., dcexec backend bash
dcexec() {
    dc exec "$@"
}

dcbash() {
    dc exec backend bash
}

# Get a shell inside the backend container.
 dcwbash() {
    dc exec worker bash
}

# Get a shell inside the frontend container.

dcfbash() {
    dc exec frontend bash
}



# List running containers for this project.
dcps() {
    dc ps
}



# --- Flask Database Migration Aliases ---
# These run inside the backend container.

# Generate a new migration script.
# e.g., migrate "add posts table"
dbmigrate() {
    dc exec backend flask db migrate -m "$1"
}

# Apply the latest migration to the database.
dbupgrade() {
    dc exec backend flask db upgrade
}


# Roll back the last migration.
dbdowngrade() {
    dc exec backend flask db downgrade
}


# Function to find and kill whatever is on a specific port
killport() {
    if [ -z "$1" ]; then
        echo "Usage: killport <port_number>"
        return 1
    fi
    
    PID=$(sudo lsof -t -i :"$1")
    
    if [ -n "$PID" ]; then
        echo "Found process with PID $PID on port $1. Terminating..."
        sudo kill -9 "$PID"
        echo "Process terminated."
    else
        echo "No process found on port $1."
    fi
}


echo "Project aliases loaded. You can now use dcup, dcdown, dcrestart, etc."