from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import get_current_user
from app.core.utils import error_responses
from app.helper.exception import (
    JoinClubNotFoundException,
    MatchNotFoundException,
    PollNotFoundException,
)
from app.rest_api.controller.poll import PollController
from app.rest_api.schema.base import CreateResponse
from app.rest_api.schema.poll import (
    CreatePollSchema,
    RetrievePollSchema,
    UpdatePollSchema,
)

poll_router = APIRouter(tags=["poll"], prefix="/poll")


@poll_router.post(
    "",
    summary="투표 생성",
    response_model=CreateResponse,
    responses={404: {"description": error_responses([PollNotFoundException])}},
)
def create_poll_of_match(
    poll_data: CreatePollSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    poll_controller = PollController(token, db)
    poll_controller.create_poll(poll_data)
    return {"success": True}


@poll_router.get(
    "/{poll_id}",
    summary="투표 상세 조회",
    response_model=RetrievePollSchema,
    responses={404: {"description": error_responses([MatchNotFoundException])}},
)
def retrieve_poll_of_match(
    poll_id: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    poll_controller = PollController(token, db)
    poll = poll_controller.retrieve_poll(poll_id)

    return poll


@poll_router.patch(
    "/{poll_id}",
    summary="투표 내용 수정",
    response_model=CreateResponse,
    responses={404: {"description": error_responses([PollNotFoundException])}},
)
def update_poll_of_match(
    poll_id: int,
    poll_data: UpdatePollSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    poll_controller = PollController(token, db)
    poll_controller.update_poll(poll_id, poll_data)
    return {"success": True}


@poll_router.delete(
    "/{poll_id}",
    summary="투표 삭제",
    response_model=CreateResponse,
    responses={404: {"description": error_responses([PollNotFoundException])}},
)
def delete_poll_of_match(
    poll_id: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    poll_controller = PollController(token, db)
    poll_controller.delete_poll(poll_id)
    return {"success": True}


@poll_router.post(
    "/{poll_id}/join",
    summary="투표 참석",
    response_model=CreateResponse,
    responses={
        404: {
            "description": error_responses(
                [PollNotFoundException, JoinClubNotFoundException]
            )
        }
    },
)
def join_poll_of_match(
    poll_id: int,
    attend: bool,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    poll_controller = PollController(token, db)
    poll_controller.join_poll(poll_id, attend)
    return {"success": True}


@poll_router.get(
    "/{poll_id}/status",
    summary="투표 진행 상태 조회",
    responses={404: {"description": error_responses([PollNotFoundException])}},
)
def get_poll_status(
    poll_id: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    poll_controller = PollController(token, db)
    poll_status = poll_controller.poll_status(poll_id)
    return poll_status
