import argparse

from db import models  # noqa: F401
from db.database import Base, engine


def init_db(drop_existing: bool = False) -> None:
    if drop_existing:
        Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create IMaMa database tables.")
    parser.add_argument(
        "--drop-existing",
        action="store_true",
        help="Drop existing tables before creating them again.",
    )
    args = parser.parse_args()

    init_db(drop_existing=args.drop_existing)
    print("Database tables are ready.")
