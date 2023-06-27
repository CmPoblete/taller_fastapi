from sqlalchemy import Column, Integer, String
from src.db.sqlalchemy import Base


class Property(Base):
    __tablename__ = "properties"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String)
    image: str = Column(String)
    address: str = Column(String)
