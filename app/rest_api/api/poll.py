from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from app.core.deps import get_db

from typing import Annotated
from app.core.token import get_current_user
from app.rest_api.schema.poll import (
    CreatePollSchema,
    RetrievePollSchema,
    UpdatePollSchema,
)
from app.rest_api.controller.poll import PollController


poll_router = APIRouter(tags=["poll"], prefix="/poll")


@poll_router.post(
    "",
    description=f"""
    **[API Description]** <br><br>
    Create poll of vote for the match <br><br>
    **[Exception List]** <br><br> 
    """,
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
    description=f"""
    **[API Description]** <br><br>
    Reterive poll of vote for the match <br><br>
    **[Exception List]** <br><br> 
    """,
    response_model=RetrievePollSchema,
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
    description=f"""
    **[API Description]** <br><br>
    Update poll of vote for the match <br><br>
    **[Exception List]** <br><br> 
    """,
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
    description=f"""
    **[API Description]** <br><br>
    Delete poll of vote for the match <br><br>
    **[Exception List]** <br><br> 
    """,
)
def delete_poll_of_match(
    poll_id: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    poll_controller = PollController(token, db)

    poll_controller.delete_poll(poll_id)
    return {"success": True}
