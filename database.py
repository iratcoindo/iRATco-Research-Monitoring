from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt

engine = create_engine("sqlite:///irm.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    fullname = Column(String)
    role = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed):
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )


def create_default_admin():

    session = Session()

    admin = session.query(User).filter_by(username="admin").first()

    if admin is None:

        admin = User(
            username="admin",
            password=hash_password("admin123"),
            fullname="Administrator",
            role="Admin"
        )

        session.add(admin)
        session.commit()

    session.close()

    research = Research(
        code="IRM-2026-001",
        title="Stem Cell Therapy for Retinitis Pigmentosa",
        principal_investigator="Prof. Kang",
        design_link="https://drive.google.com/.....",
        progress=35,
        owner="admin"
    )
    
    session.add(research)
    session.commit()

class Research(Base):
    __tablename__ = "research"

    id = Column(Integer, primary_key=True)

    code = Column(String)

    title = Column(String)

    principal_investigator = Column(String)

    design_link = Column(String)

    progress = Column(Integer)

    owner = Column(String)
