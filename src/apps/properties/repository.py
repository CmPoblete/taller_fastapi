from abc import ABC, abstractmethod
from src.apps.properties.models import Property
from src.models.property import Property as PropertySQLAlchemy
from src.db.db import properties
from src.db.sqlalchemy import engine
from sqlalchemy.orm import Session
from src.db.mongo import db
from bson.objectid import ObjectId


class PropertyRepositoryBase(ABC):
    @classmethod
    @abstractmethod
    def get_all(cls) -> list[Property]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def filter(cls, attribute: str, param: str) -> list[Property]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create_property(cls, property_params: Property) -> list[Property]:
        raise NotImplementedError


class PropertyRepository(PropertyRepositoryBase):
    db = properties

    @classmethod
    def get_all(cls) -> list[Property]:
        return [Property(**prop) for prop in cls.db]

    @classmethod
    def filter(cls, attribute: str, param: str) -> list[Property]:
        return [
            Property(**prop)
            for prop in filter(lambda prop: prop[attribute] == param, cls.db)
        ]

    @classmethod
    def create_property(cls, property_params: Property) -> list[Property]:
        cls.db.append(property_params.dict())
        return [Property(**prop) for prop in cls.db]


class PropertySQLAlchemyRepository(PropertyRepositoryBase):
    @classmethod
    def get_all(cls) -> list[Property]:
        with Session(engine) as session:
            return [
                Property.from_orm(prop)
                for prop in session.query(PropertySQLAlchemy).all()
            ]

    @classmethod
    def filter(cls, attribute: str, param: str) -> list[Property]:
        with Session(engine) as session:
            return [
                Property.from_orm(prop)
                for prop in session.query(PropertySQLAlchemy).filter(
                    getattr(PropertySQLAlchemy, attribute) == param
                )
            ]

    @classmethod
    def create_property(cls, property_params: Property) -> list[Property]:
        with Session(engine) as session:
            new_property = PropertySQLAlchemy(**property_params.dict())
            session.add(new_property)
            session.commit()
            session.refresh(new_property)
            return cls.get_all()


class PropertyMongoRepository(PropertyRepositoryBase):
    db = db.get_collection("properties")

    @classmethod
    def get_all(cls) -> list[Property]:
        properties = cls.db.find()
        return [Property(**prop) for prop in properties]

    @classmethod
    def filter(cls, attribute: str, param: str) -> list[Property]:
        param = param if attribute != "id" else ObjectId(param)
        attribute = attribute if attribute != "id" else "_id"
        properties = cls.db.find({attribute: param})
        return [Property(**prop) for prop in properties]

    @classmethod
    def create_property(cls, property_params: Property) -> list[Property]:
        property_obj = property_params.dict()
        cls.db.insert_one(property_obj)
        return cls.get_all()
