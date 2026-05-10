from sqlmodel import SQLModel, Session, create_engine, select
from pages.helper.data_models import MissingPerson, PublicSubmissions

DATABASE_URL = "sqlite:///sqlite_database.db"
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Auto-create on import
create_db_and_tables()


# ── Missing Persons ──────────────────────────────────────────────────────────

def new_missing_case(person: MissingPerson):
    with Session(engine) as session:
        session.add(person)
        session.commit()
        session.refresh(person)
    return person


def get_all_missing_cases():
    with Session(engine) as session:
        return session.exec(select(MissingPerson)).all()


def get_registered_cases_count(registered_by: str, status: str):
    with Session(engine) as session:
        statement = select(MissingPerson).where(
            MissingPerson.registered_by == registered_by,
            MissingPerson.status == status,
        )
        return session.exec(statement).all()


def get_missing_person_by_id(person_id: str):
    with Session(engine) as session:
        return session.get(MissingPerson, person_id)


def update_missing_person_status(person_id: str, status: str):
    with Session(engine) as session:
        person = session.get(MissingPerson, person_id)
        if person:
            person.status = status
            session.add(person)
            session.commit()


def delete_missing_person(person_id: str):
    with Session(engine) as session:
        person = session.get(MissingPerson, person_id)
        if person:
            session.delete(person)
            session.commit()


# ── Public Submissions ───────────────────────────────────────────────────────

def new_public_case(submission: PublicSubmissions):
    with Session(engine) as session:
        session.add(submission)
        session.commit()
        session.refresh(submission)
    return submission


def get_all_public_submissions():
    with Session(engine) as session:
        return session.exec(select(PublicSubmissions)).all()


def get_public_submission_by_id(sub_id: str):
    with Session(engine) as session:
        return session.get(PublicSubmissions, sub_id)
