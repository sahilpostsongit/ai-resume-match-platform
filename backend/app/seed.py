from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import Job

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "jobs.csv"


def seed_jobs(session: Session) -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Seed data missing at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    for _, row in df.iterrows():
        exists = session.query(Job).filter(Job.title == row["title"], Job.company == row["company"]).first()
        if exists:
            continue
        job = Job(
            title=row["title"],
            company=row["company"],
            location=row["location"],
            description=row["description"],
            requirements=row["requirements"],
        )
        session.add(job)
    session.commit()


def main():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        seed_jobs(session)
    print("Seeded jobs successfully.")


if __name__ == "__main__":
    main()





