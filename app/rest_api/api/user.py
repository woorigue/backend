from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import create_access_token, create_refresh_token, verify_password
from app.model.user import User
from app.rest_api.controller.user import user_controller as con
from app.rest_api.schema.base import CreateResponse
from app.rest_api.schema.user import EmailLoginSchema, EmailRegisterSchema

user_router = APIRouter(tags=["user"], prefix="/user")


@user_router.post("/email/register", response_model=CreateResponse)
def email_register_user(user_data: EmailRegisterSchema, db: Session = Depends(get_db)):
    con.email_register_user(db, user_data)
    return {"success": True}


@user_router.post("/email/login")
def email_login(user_data: EmailLoginSchema, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == user_data.email))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    result = verify_password(user_data.password, user.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password is not matched",
        )

    access_token = create_access_token(data={"sub": str(user_data.email)})
    refresh_token = create_refresh_token(data={"sub": str(user_data.email)})

    return {"access_token": access_token, "refresh_token": refresh_token}
