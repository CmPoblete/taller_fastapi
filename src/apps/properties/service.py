from src.apps.properties.models import Property
from src.apps.properties.repository import PropertyRepositoryBase


class PropertyService:
    def __init__(self, repository: PropertyRepositoryBase) -> None:
        self.repository = repository

    def get_all(self) -> list[Property]:
        return self.repository.get_all()

    def filter_by_name(self, name: str) -> list[Property]:
        return self.repository.filter(attribute="name", param=name)

    def create_property(self, property_params: Property) -> list[Property]:
        return self.repository.create_property(property_params=property_params)

    def get_by_id(self, id: int) -> Property | None:
        property_filter = self.repository.filter(attribute="id", param=id)
        if property_filter:
            return property_filter[0]
        return None
