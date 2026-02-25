from sqlalchemy import create_engine, text

# Your specific URL
DATABASE_URL = "postgresql://postgres:BBenjamin%402004@localhost:5432/supply_chain_ai"

# Create the engine (the "key" to open the DB)
engine = create_engine(DATABASE_URL)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Connection Successful!")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_connection()