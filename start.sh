#!/bin/bash
# Iniciar el servidor Flask en background
gunicorn main:app --bind 0.0.0.0:$PORT &

# Iniciar el bot en el mismo contenedor
python3 main.py
