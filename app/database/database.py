from sqlmodel import SQLModel, Session, create_engine

urlBD = "sqlite:///quiz.db"

engine = create_engine(DATABASE_URL, echo=False)


def crear_tablas():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)