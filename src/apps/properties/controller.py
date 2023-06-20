from src.apps.properties.models import Property, PropertyInput
from fastapi import APIRouter, Depends
from src.apps.properties.repository import (
    PropertyMongoRepository,
    PropertyRepository,
    PropertySQLAlchemyRepository,
)
from src.apps.properties.service import PropertyService

router = APIRouter()


@router.get("/properties")
def get_properties(
    name: str | None = None,
    service: PropertyService = Depends(
        lambda: PropertyService(repository=PropertyMongoRepository())
    ),
) -> list[Property]:
    if name:
        return service.filter_by_name(name=name)
    return service.get_all()


@router.get("/properties/{property_id}")
def get_property(
    property_id: int | str,
    service: PropertyService = Depends(
        lambda: PropertyService(repository=PropertyMongoRepository())
    ),
) -> Property | None:
    return service.get_by_id(id=property_id)


@router.post("/properties")
def create_property(
    property: PropertyInput,
    service: PropertyService = Depends(
        lambda: PropertyService(repository=PropertyMongoRepository())
    ),
) -> list[Property]:
    return service.create_property(property_params=property)
