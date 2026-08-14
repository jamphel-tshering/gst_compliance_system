#!/bin/bash
# Backup script for Render.com deployment

BACKUP_DIR="/opt/render/project/backups"
DB_PATH="/opt/render/project/src/db.sqlite3"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/gst_compliance_backup_$TIMESTAMP.db"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Copy database
cp "$DB_PATH" "$BACKUP_FILE"

# Keep only last 7 backups
cd "$BACKUP_DIR"
ls -t gst_compliance_backup_*.db | tail -n +8 | xargs -r rm

echo "Backup created: $BACKUP_FILE"
