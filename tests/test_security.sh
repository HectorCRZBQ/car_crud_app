#!/bin/bash

# Variables de entorno
PROJECT_DIR=$(pwd)
IMAGE_NAME="car-app"

echo "==> Iniciando pruebas de seguridad con Trivy"

# 1. Escaneo de dependencias
echo "==> Escaneando vulnerabilidades en dependencias (requirements.txt)"
trivy fs --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed --no-progress "${PROJECT_DIR}" || {
    echo "❌ Vulnerabilidades críticas detectadas en las dependencias"
    exit 1
}
echo "✅ No se detectaron vulnerabilidades críticas en las dependencias"

# 2. Escaneo de imagen Docker (opcional)
if [[ $(docker images -q "${IMAGE_NAME}") ]]; then
    echo "==> Escaneando vulnerabilidades en la imagen Docker (${IMAGE_NAME})"
    trivy image --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed --no-progress "${IMAGE_NAME}" || {
        echo "❌ Vulnerabilidades críticas detectadas en la imagen Docker"
        exit 1
    }
    echo "✅ No se detectaron vulnerabilidades críticas en la imagen Docker"
else
    echo "⚠️ Imagen Docker (${IMAGE_NAME}) no encontrada. Saltando escaneo de contenedor."
fi

echo "✅ Todas las pruebas de seguridad pasaron satisfactoriamente"
