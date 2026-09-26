#!/bin/bash
# Desplegament al VPS. L'executa el workflow .github/workflows/deploy.yml des
# del directori del repo (/app/sapa/inventory) després del git pull.
#
#  1. Crea el .env de producció si no existeix (SECRET_KEY nova, DEBUG=False).
#  2. Migració única des de la instal·lació antiga (runserver, dades dins del
#     contenidor): atura el contenidor antic, en copia la BD i media als volums
#     i el conserva aturat com a "inventory-legacy" per si cal tornar enrere.
#  3. Còpia de seguretat prèvia al desplegament.
#  4. Build + up, espera que el contenidor estigui "healthy" i recarrega el proxy.
set -euo pipefail

cd "$(dirname "$0")/.."
APP_DIR=$(pwd)
PROXY_CONTAINER=${PROXY_CONTAINER:-proxy-nginx-nginx-1}
DOMAIN=${DOMAIN:-inventari.asixsapa.cat}
STAMP=$(date +%Y%m%d-%H%M%S)
APP_UID=1000

mkdir -p backups/daily
chmod 700 backups
# Les còpies diàries les escriu el servei "backup" amb l'uid de l'app
chown "$APP_UID:$APP_UID" backups/daily 2>/dev/null || true
chmod 700 backups/daily

# --- 1. .env ------------------------------------------------------------------
if [ ! -f .env ]; then
  echo "🔑 Creant .env de producció amb una SECRET_KEY nova"
  KEY=$(openssl rand -base64 48 | tr -d '\n/+=' | cut -c1-60)
  sed -e "s|^SECRET_KEY=.*|SECRET_KEY=$KEY|" .env.example > .env
  chmod 600 .env
fi
if grep -qE '^DEBUG=True' .env; then
  echo "❌ El .env té DEBUG=True: no es desplega amb DEBUG actiu a producció"
  exit 1
fi

echo "🔎 Validant docker-compose.yml i .env..."
docker compose config -q

# --- 2. Migració des de la instal·lació antiga ---------------------------------
volume_has_db() {
  docker run --rm -v inventory_data:/data:ro alpine:3.20 test -f /data/db.sqlite3
}

if docker container inspect inventory >/dev/null 2>&1 \
   && docker exec inventory test -f /app/inventory/db.sqlite3 2>/dev/null; then
  if volume_has_db; then
    echo "❌ Hi ha un contenidor antic amb dades i el volum ja té una BD. Revisa-ho a mà."
    exit 1
  fi
  LEGACY_DIR="backups/legacy-$STAMP"
  echo "📦 Migrant dades de la instal·lació antiga a $LEGACY_DIR i als volums"
  docker stop inventory
  mkdir -p "$LEGACY_DIR"
  docker cp inventory:/app/inventory/db.sqlite3 "$LEGACY_DIR/db.sqlite3"
  docker cp inventory:/app/inventory/media "$LEGACY_DIR/media"
  chmod -R go-rwx "$LEGACY_DIR"
  docker run --rm \
    -v inventory_data:/data -v inventory_media:/media \
    -v "$APP_DIR/$LEGACY_DIR:/src:ro" alpine:3.20 sh -c "
      cp /src/db.sqlite3 /data/db.sqlite3 &&
      cp -a /src/media/. /media/ &&
      chown -R $APP_UID:$APP_UID /data /media"
  docker rename inventory inventory-legacy
  echo "   Contenidor antic conservat (aturat) com a inventory-legacy"
fi

# --- 3. Còpia prèvia ---------------------------------------------------------------
if volume_has_db; then
  echo "💾 Còpia de la BD abans de desplegar"
  docker run --rm -v inventory_data:/data:ro -v "$APP_DIR/backups:/b" alpine:3.20 \
    sh -c "cp /data/db.sqlite3 /b/pre-deploy-$STAMP.sqlite3 && chmod 600 /b/pre-deploy-$STAMP.sqlite3"
  ls -1t backups/pre-deploy-*.sqlite3 2>/dev/null | tail -n +11 | xargs -r rm -f
fi

# --- 4. Build i arrencada ------------------------------------------------------
echo "🐳 Construint i arrencant"
docker compose build --pull web
docker compose up -d --remove-orphans

echo "🩺 Esperant que l'aplicació estigui sana..."
STATUS=unknown
for _ in $(seq 1 36); do
  STATUS=$(docker inspect -f '{{.State.Health.Status}}' inventory 2>/dev/null || echo missing)
  [ "$STATUS" = "healthy" ] && break
  sleep 5
done
if [ "$STATUS" != "healthy" ]; then
  echo "❌ L'aplicació no ha arrencat (estat: $STATUS). Últims logs:"
  docker compose logs --tail 60 web || true
  exit 1
fi

# El proxy resol "inventory" en arrencar: recarregar-lo perquè agafi la IP nova
echo "🔁 Recarregant el proxy nginx"
docker exec "$PROXY_CONTAINER" nginx -t
docker exec "$PROXY_CONTAINER" nginx -s reload
sleep 2

HTTP=$(docker exec "$PROXY_CONTAINER" curl -sk -o /dev/null -w '%{http_code}' \
  --resolve "$DOMAIN:443:127.0.0.1" "https://$DOMAIN/healthz" || true)
echo "   https://$DOMAIN/healthz → $HTTP"
if [ "$HTTP" != "200" ]; then
  echo "❌ El proxy no arriba a l'aplicació"
  exit 1
fi

echo "✅ Desplegament completat"
