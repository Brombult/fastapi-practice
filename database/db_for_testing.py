from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

TEST_DATABASE_URL = f"postgresql://{settings.user}:{settings.password}@{settings.host}/{settings.database}_test"

engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
