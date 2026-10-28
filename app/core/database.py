from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# For SQLite, check_same_thread=False is needed for multi-threaded access
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    echo=(settings.ENVIRONMENT == "development"),
    connect_args=connect_args
)

def init_db():
    # Import models so SQLModel metadata registers all tables
    import app.models  # noqa: F401
    SQLModel.metadata.create_all(engine)

# Auto-initialize tables on import
init_db()

def get_session():
    with Session(engine) as session:
        yield session
