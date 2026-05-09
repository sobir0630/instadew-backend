#!/bin/bash

echo "🔥 RESET STARTED..."

# =========================================
# DELETE DATABASE
# =========================================
if [ -f db.sqlite3 ]; then
    rm db.sqlite3
    echo "✅ db.sqlite3 deleted"
else
    echo "⚠️ db.sqlite3 not found"
fi

# =========================================
# DELETE MEDIA
# =========================================
if [ -d media ]; then
    rm -rf media
    echo "✅ media folder deleted"
else
    echo "⚠️ media folder not found"
fi

# recreate media
mkdir media

# =========================================
# DELETE MIGRATIONS
# =========================================
echo "⏳ deleting migrations..."

find . -path "*/migrations/*.py" ! -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# =========================================
# DELETE __pycache__
# =========================================
echo "⏳ deleting __pycache__..."

find . -type d -name "__pycache__" -exec rm -rf {} +

# =========================================
# MAKE MIGRATIONS
# =========================================
echo "⏳ making migrations..."

python manage.py makemigrations

# =========================================
# MIGRATE
# =========================================
echo "⏳ migrating..."

python manage.py migrate

echo ""
echo "🚀 FULL PROJECT RESET COMPLETE"