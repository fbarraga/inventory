# Imatge de producció de l'aplicació d'inventari (Django + gunicorn)
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

FROM python:3.12-slim

LABEL name="inventoryapp"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/opt/venv/bin:$PATH \
    DATA_DIR=/app/data \
    MEDIA_ROOT=/app/media

# Usuari sense privilegis (uid fix perquè els volums tinguin propietari estable)
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --no-create-home --shell /usr/sbin/nologin app

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app . .

# Estàtics recollits a la imatge (clau temporal: collectstatic no la fa servir)
RUN SECRET_KEY=build-only python manage.py collectstatic --noinput \
    && mkdir -p /app/data /app/media/qr_codes /app/media/inventario_fotos \
    && chown -R app:app /app/data /app/media /app/staticfiles \
    && chmod +x /app/entrypoint.sh

USER app

EXPOSE 7000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:7000/healthz', timeout=4).status == 200 else 1)"

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7000", "--workers", "3", "--timeout", "60", "--access-logfile", "-", "--forwarded-allow-ips", "*"]
