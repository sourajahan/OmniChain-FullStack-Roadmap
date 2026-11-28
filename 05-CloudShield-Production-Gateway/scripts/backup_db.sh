#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p "${BACKUP_DIR}"

if [[ -n "${DATABASE_URL:-}" ]]; then
  OUT_FILE="${BACKUP_DIR}/omnichain_${TIMESTAMP}.sql.gz"
  pg_dump "${DATABASE_URL}" | gzip > "${OUT_FILE}"
  echo "Created PostgreSQL backup: ${OUT_FILE}"
else
  echo "DATABASE_URL is not set; skipping remote pg_dump."
fi

find "${BACKUP_DIR}" -type f -name "*.gz" -mtime +"${RETENTION_DAYS}" -delete
