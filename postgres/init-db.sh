#!/bin/bash
set -e
set -x

echo "******PostgreSQL initialisation******"
pg_restore -C -a -d movies -U postgres /var/lib/postgresql/backup/db.dump
