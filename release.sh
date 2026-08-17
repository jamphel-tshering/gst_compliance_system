#!/bin/bash
# Release script for Render - runs migrations on PostgreSQL
python manage.py migrate --noinput