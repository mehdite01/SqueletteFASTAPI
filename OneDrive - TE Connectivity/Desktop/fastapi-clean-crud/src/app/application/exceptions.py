class ApplicationError(Exception):
    code = "APPLICATION_ERROR"
    status_code = 400

    def __init__(
        self,
        message: str,
        details: object | None = None,
    ) -> None:
        self.message = message
        self.details = details

        super().__init__(message)


class EntityNotFoundError(ApplicationError):
    code = "ENTITY_NOT_FOUND"
    status_code = 404

    def __init__(
        self,
        entity_name: str,
        entity_id: object,
    ) -> None:
        self.entity_name = entity_name
        self.entity_id = entity_id

        super().__init__(
            message=(
                f"{entity_name} with id "
                f"'{entity_id}' was not found."
            )
        )