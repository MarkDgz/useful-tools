#!/bin/bash

# Created By Mark Dgz (tnemexico@gmail.com) with ChatGPT 4.0
# August 4, 2024.

# Definir la carpeta de Descargas, setting Downloads path
DOWNLOADS_DIR="$HOME/Descargas"

# Buscar todos los archivos .deb relacionados con Discord en la carpeta Descargas
# Search all discord*.deb files into Downloads path
DISCORD_DEB_FILES=($(ls -t $DOWNLOADS_DIR/discord*.deb))

# Verificar si hay archivos .deb encontrados
# Verifying if .deb files exists
if [ ${#DISCORD_DEB_FILES[@]} -eq 0 ]; then
    echo "No se encontraron archivos .deb de Discord en $DOWNLOADS_DIR."
    exit 1
fi

# Mantener solo el archivo más reciente y eliminar el resto
# Keep the last discord*.db file in order to apply discord update
LATEST_FILE=${DISCORD_DEB_FILES[0]}
for FILE in "${DISCORD_DEB_FILES[@]:1}"; do
    echo "Eliminando archivo antiguo: $FILE"
    rm "$FILE"
done

# Instalar el archivo .deb más reciente
# Installing current .deb file downloaded
echo "Instalando el archivo más reciente: $LATEST_FILE"
sudo dpkg -i "$LATEST_FILE"

# Limpiar paquetes que puedan haber quedado rotos
# Fixing broken packages
sudo apt-get install -f

echo "Actualización de Discord completada."
