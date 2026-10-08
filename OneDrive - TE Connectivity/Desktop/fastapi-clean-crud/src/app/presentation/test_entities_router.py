from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status

from app.application.test_entities.create_test_entity import (
    CreateTestEntityUseCase,
)
from app.application.test_entities.delete_test_entity import (
    DeleteTestEntityUseCase,
)
from app.application.test_entities.get_test_entity import (
    GetTestEntityUseCase,
)
from app.application.test_entities.list_test_entities import (
    ListTestEntitiesUseCase,
)
from app.application.test_entities.schemas import (
    CreateTestEntityRequest,
    UpdateTestEntityRequest,
)
from app.application.test_entities.schemas import (
    TestEntityPageResponse as EntityPageResponseSchema,
)
from app.application.test_entities.schemas import (
    TestEntityResponse as EntityResponseSchema,
)
from app.application.test_entities.update_test_entity import (
    UpdateTestEntityUseCase,
)
from app.domain.repositories.query import (
    Query as DomainQuery,
)
from app.domain.repositories.query import (
    Sort,
)
from app.domain.unit_of_work import UnitOfWork
from app.presentation.dependencies import get_unit_of_work
from app.presentation.responses import (
    ApiPageResponse,
    ApiResponse,
)

router = APIRouter(
    prefix="/test-entities",
    tags=["Test Entities"],
)


@router.post(
    "",
    response_model=ApiResponse[EntityResponseSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_test_entity(
    request: CreateTestEntityRequest,
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
) -> ApiResponse[EntityResponseSchema]:
    use_case = CreateTestEntityUseCase(
        unit_of_work,
    )

    entity = await use_case.execute(
        name=request.name,
    )

    return ApiResponse(
        data=EntityResponseSchema.model_validate(
            entity,
        ),
    )


@router.get(
    "/{entity_id}",
    response_model=ApiResponse[EntityResponseSchema],
)
async def get_test_entity(
    entity_id: UUID,
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
) -> ApiResponse[EntityResponseSchema]:
    use_case = GetTestEntityUseCase(
        unit_of_work,
    )

    entity = await use_case.execute(
        entity_id,
    )

    from app.application.exceptions import (
        EntityNotFoundError,
    )

    if entity is None:
        raise EntityNotFoundError(
            "TestEntity",
            entity_id,
        )

    return ApiResponse(
        data=EntityResponseSchema.model_validate(
            entity,
        ),
    )


@router.put(
    "/{entity_id}",
    response_model=ApiResponse[EntityResponseSchema],
)
async def update_test_entity(
    entity_id: UUID,
    request: UpdateTestEntityRequest,
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
) -> ApiResponse[EntityResponseSchema]:
    use_case = UpdateTestEntityUseCase(
        unit_of_work,
    )

    entity = await use_case.execute(
        entity_id=entity_id,
        name=request.name,
    )

    return ApiResponse(
        data=EntityResponseSchema.model_validate(
            entity,
        ),
    )


@router.delete(
    "/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_test_entity(
    entity_id: UUID,
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
) -> Response:
    use_case = DeleteTestEntityUseCase(
        unit_of_work,
    )

    await use_case.execute(
        entity_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.get(
    "",
    response_model=ApiPageResponse[
        EntityResponseSchema
    ],
)
async def list_test_entities(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    sort_field: str = Query(
        default="id",
    ),
    descending: bool = Query(
        default=False,
    ),
    unit_of_work: UnitOfWork = Depends(
        get_unit_of_work,
    ),
) -> ApiPageResponse[EntityResponseSchema]:
    use_case = ListTestEntitiesUseCase(
        unit_of_work,
    )

    query = DomainQuery(
        page=page,
        page_size=page_size,
        sort=Sort(
            field=sort_field,
            descending=descending,
        ),
    )

    result = await use_case.execute(
        query,
    )

    return ApiPageResponse(
        data=[
            EntityResponseSchema.model_validate(
                entity,
            )
            for entity in result.items
        ],
        page=result.page,
        page_size=result.page_size,
        total=result.total,
        total_pages=result.total_pages,
    )