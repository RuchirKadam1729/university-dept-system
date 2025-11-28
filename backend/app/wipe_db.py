#usage: docker compose exec backend python -m app.wipe_db
from app.database import engine, Base
from sqlalchemy import text

print("🗑️  Wiping database...")

# Drop all tables
Base.metadata.drop_all(bind=engine)
print("   ✓ All tables dropped")

# Recreate all tables (empty)
Base.metadata.create_all(bind=engine)
print("   ✓ Tables recreated (empty)")

print("✅ Database wiped successfully!")
print("\n💡 Tip: Run 'docker compose exec backend python -m app.seed' to repopulate with sample data")