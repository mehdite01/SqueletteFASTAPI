from app.domain.entities.test_entity import TestEntity as TestEntityDomain
from app.infrastructure.database.mappers.base_mapper import BaseMapper
from app.infrastructure.database.models.entity_model import (
    TestEntity as TestEntityModel,
)


class TestEntityMapper(
    BaseMapper[TestEntityDomain, TestEntityModel]
):
    def to_model(
        self,
        entity: TestEntityDomain,
    ) -> TestEntityModel:
        return TestEntityModel(
            id=entity.id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(
        self,
        model: TestEntityModel,
    ) -> TestEntityDomain:
        return TestEntityDomain(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )