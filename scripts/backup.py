"""Còpia diària de la BD SQLite (API de backup, consistent en calent) i de media.

S'executa al servei "backup" del docker-compose, sense xarxa i amb les dades
muntades només lectura. Conserva les còpies BACKUP_KEEP_DAYS dies.
"""
import gzip
import os
import shutil
import sqlite3
import tarfile
import time
from datetime import datetime
from pathlib import Path

DATA = Path("/data/db.sqlite3")
MEDIA = Path("/media")
DEST = Path("/backups")
KEEP_DAYS = int(os.getenv("BACKUP_KEEP_DAYS", "30"))


def backup_once():
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    if not DATA.exists():
        print("No hi ha BD a copiar", flush=True)
        return
    tmp = DEST / f"db-{stamp}.sqlite3"
    src = sqlite3.connect(f"file:{DATA}?mode=ro", uri=True)
    dst = sqlite3.connect(tmp)
    with dst:
        src.backup(dst)
    src.close()
    dst.close()
    with open(tmp, "rb") as f_in, gzip.open(f"{tmp}.gz", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    tmp.unlink()
    with tarfile.open(DEST / f"media-{stamp}.tar.gz", "w:gz") as tar:
        tar.add(MEDIA, arcname="media")
    for f in DEST.glob(f"*-{stamp}*"):
        f.chmod(0o600)
    print(f"Còpia feta: {stamp}", flush=True)


def prune():
    limit = time.time() - KEEP_DAYS * 86400
    for pattern in ("db-*.sqlite3.gz", "media-*.tar.gz"):
        for f in DEST.glob(pattern):
            if f.stat().st_mtime < limit:
                f.unlink()


if __name__ == "__main__":
    while True:
        try:
            backup_once()
            prune()
        except Exception as exc:  # no aturar el bucle per un error puntual
            print(f"Error a la còpia: {exc}", flush=True)
        time.sleep(86400)
