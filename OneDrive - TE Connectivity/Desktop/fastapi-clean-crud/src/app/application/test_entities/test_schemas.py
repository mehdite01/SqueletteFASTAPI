from pydantic import ValidationError

from app.application.test_entities.schemas import (
    CreateTestEntityRequest,
)
from app.application.test_entities.schemas import (
    TestEntityResponse as EntityResponseSchema,
)


def main() -> None:
    valid_request = CreateTestEntityRequest(
        name="Product A"
    )

    print("VALID REQUEST:", valid_request)

    try:
        CreateTestEntityRequest(
            name=""
        )
    except ValidationError as exception:
        print("EMPTY NAME REJECTED")
        print(exception)

    try:
        CreateTestEntityRequest(
            name="A" * 101
        )
    except ValidationError as exception:
        print("TOO LONG NAME REJECTED")
        print(exception)

    print(
        "RESPONSE MODEL:",
        EntityResponseSchema.model_fields,
    )


if __name__ == "__main__":
    main()