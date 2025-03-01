# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.db_models.DbProfile import Base, DbProfile

DATABASE_URL = "sqlite:///profiles.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database and seed it if empty."""
    Base.metadata.create_all(bind=engine)
    seed_db()


def seed_db():
    """Seed the database with dummy profiles if no records exist."""
    session = SessionLocal()
    # Check if any profiles exist in the database.
    first_exist = session.query(DbProfile).first()
    if first_exist:
        print("Database already seeded.")
        session.close()
        return

    # Define some dummy profiles using a hybrid approach.
    profiles = [
        DbProfile(
            name="John Doe",
            phone="1234567890",
            email="john.doe@example.com",
            summary="Experienced software engineer.",
            extra_data={
                "skills": ["Python", "SQLAlchemy", "Flask"],
                "experience": ["Software Engineer at Company A", "Senior Developer at Company B"],
                "education": ["B.Sc. in Computer Science from University X"],
                "another_info": "Loves coding and open-source."
            }
        ),
        DbProfile(
            name="Jane Smith",
            phone="0987654321",
            email="jane.smith@example.com",
            summary="Data scientist and AI enthusiast.",
            extra_data={
                "skills": ["Python", "Pandas", "Machine Learning"],
                "experience": ["Data Scientist at Company C"],
                "education": ["M.Sc. in Data Science from University Y"],
                "another_info": "Enjoys analyzing big data and building predictive models."
            }
        ),
        DbProfile(
            name="Alice Johnson",
            phone="5551234567",
            email="alice.johnson@example.com",
            summary="Frontend developer with a passion for design.",
            extra_data={
                "skills": ["JavaScript", "React", "CSS"],
                "experience": ["Frontend Developer at Startup Z"],
                "education": ["B.A. in Graphic Design from University Z"],
                "another_info": "Combines creativity with coding."
            }
        )
    ]

    session.add_all(profiles)
    session.commit()
    session.close()
    print("Database seeded successfully.")
