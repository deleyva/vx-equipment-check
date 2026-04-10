#!/bin/bash

# Script para crear y publicar un release completo de Comprobación de PC Vitalinux

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Comprobación de PC Vitalinux - Release Helper${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Error: No se encontró package.json. Ejecuta este script desde el directorio raíz del proyecto.${NC}"
    exit 1
fi

# Obtener versión actual
CURRENT_VERSION=$(node -pe "require('./package.json').version")
echo -e "${YELLOW}📋 Versión actual: v${CURRENT_VERSION}${NC}"

# Preguntar por nueva versión
echo ""
read -p "🔢 Nueva versión (ejemplo: 1.0.7): " NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    echo -e "${RED}❌ Error: Debes especificar una versión.${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}📝 Proceso de release:${NC}"
echo "1. Actualizar package.json a v${NEW_VERSION}"
echo "2. Construir con Docker"
echo "3. Crear tag y push"
echo "4. GitHub creará draft release automáticamente"
echo "5. Subir archivos al release"
echo ""

read -p "¿Continuar? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⏹️  Cancelado por el usuario.${NC}"
    exit 0
fi

# Paso 1: Actualizar versión en package.json
echo ""
echo -e "${BLUE}📝 Paso 1: Actualizando package.json...${NC}"
sed -i.bak "s/\"version\": \"$CURRENT_VERSION\"/\"version\": \"$NEW_VERSION\"/" package.json
rm package.json.bak
echo -e "${GREEN}✅ Versión actualizada a v${NEW_VERSION}${NC}"

# Paso 2: Construir con Docker
echo ""
echo -e "${BLUE}🐳 Paso 2: Construyendo con Docker...${NC}"
if [ -f "./docker-build.sh" ]; then
    ./docker-build.sh
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Build completado exitosamente${NC}"
    else
        echo -e "${RED}❌ Error en el build. Revisa los logs arriba.${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Error: No se encontró docker-build.sh${NC}"
    exit 1
fi

# Paso 3: Git commit, tag y push
echo ""
echo -e "${BLUE}📤 Paso 3: Creando tag y push...${NC}"
git add package.json
git commit -m "Bump version to v${NEW_VERSION}"
git push

git tag "v${NEW_VERSION}"
git push origin "v${NEW_VERSION}"
echo -e "${GREEN}✅ Tag v${NEW_VERSION} creado y pusheado${NC}"

# Paso 4: Esperar a que GitHub Actions cree el draft
echo ""
echo -e "${BLUE}⏳ Paso 4: GitHub Actions creará el draft release...${NC}"
echo "🔗 Ve a: https://github.com/deleyva/vx-dga-pc-check-form/releases"
echo ""

# Paso 5: Mostrar archivos para subir
echo -e "${BLUE}📦 Paso 5: Archivos listos para subir al release:${NC}"
if [ -d "./docker-output" ]; then
    echo ""
    find ./docker-output -name "*.deb" -o -name "*.rpm" -o -name "*.AppImage" | while read file; do
        size=$(ls -lh "$file" | awk '{print $5}')
        echo -e "${GREEN}📁 $file${NC} (${size})"
    done
    echo ""
    echo -e "${YELLOW}📋 Pasos finales:${NC}"
    echo "1. Ve al draft release en GitHub"
    echo "2. Arrastra y suelta los archivos de ./docker-output/"
    echo "3. Publica el release"
else
    echo -e "${RED}❌ No se encontró el directorio docker-output${NC}"
fi

echo ""
echo -e "${GREEN}🎉 ¡Release v${NEW_VERSION} preparado!${NC}"
