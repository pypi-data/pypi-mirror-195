import asyncio
import dataclasses
import functools
from pydantic import BaseModel
from business_validator import (
    Validator,
    ValidationError,
    ValidationContext,
    ErrorSchema,
    ErrorCodeEnum,
    validate,
)


class CommentDto(BaseModel):
    comment: str
    post_id: int
    owner_id: int


class Source(BaseModel):
    local: str
    position: int


class CustomValidationContext(ValidationContext[ErrorSchema[Source]]):
    is_approved: bool = False


@dataclasses.dataclass()
class CommentValidator(Validator[ErrorSchema[Source]]):
    dto_list: list[CommentDto]

    @functools.cached_property
    def context(self) -> CustomValidationContext:
        return CustomValidationContext()

    @validate()
    async def test1(self):
        post_ids = range(1, 10)
        for i, dto in enumerate(self.dto_list):
            if dto.post_id not in post_ids:
                self.context.add_error(
                    ErrorSchema(
                        code=ErrorCodeEnum.not_found.value,
                        message="Id doen't not exists",
                        detail=f"Post with id={dto.post_id} not found",
                        source=Source(
                            local="data/post_id",
                            position=i,
                        ),
                    )
                )

    @validate()
    async def test2(self):
        owner_ids = range(1, 10)
        for i, dto in enumerate(self.dto_list):
            if dto.owner_id not in owner_ids:
                self.context.add_error(
                    ErrorSchema(
                        code=ErrorCodeEnum.not_found.value,
                        message="Id doen't not exists",
                        detail=f"User with id={dto.post_id} not found",
                        source=Source(
                            local="data/owner_id",
                            position=i,
                        ),
                    )
                )


async def main():
    dto_list = [
        CommentDto(comment="comment", owner_id=1, post_id=1),
        CommentDto(comment="comment", owner_id=1, post_id=100),
        CommentDto(comment="comment", owner_id=100, post_id=1),
        CommentDto(comment="comment", owner_id=1234, post_id=1234),
    ]
    try:
        await CommentValidator(dto_list).validate()
    except ValidationError as e:
        for message in e.messages:
            print(message)


if __name__ == "__main__":
    asyncio.run(main())
