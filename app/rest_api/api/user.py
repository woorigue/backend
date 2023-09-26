from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    validate_refresh_token,
    verify_password,
)
from app.helper.exception import ProfileRequired
from app.model.position import JoinPosition
from app.model.user import User
from app.rest_api.controller.email import email_controller as email_con
from app.rest_api.controller.user import user_controller as con
from app.rest_api.schema.base import CreateResponse
from app.rest_api.schema.email import (
    EmailAuthCodeSchema,
    EmailPasswordResetSchema,
    EmailVerifySchema,
)
from app.rest_api.schema.profile import UpdateProfileSchema
from app.rest_api.schema.token import RefreshTokenSchema
from app.rest_api.schema.user import (
    EmailLoginSchema,
    EmailRegisterSchema,
    ResetPasswordSchema,
    UserSchema,
)
from app.constants.errors import (
    EMAIL_CONFLICT_SYSTEM_CODE,
    EMAIL_VERIFY_CODE_EXPIRED_SYSTEM_CODE,
    PASSWORD_INVALID_SYSTEM_CODE,
    EMAIL_AUTH_NUMBER_INVALID_SYSTEM_CODE,
)

user_router = APIRouter(tags=["user"], prefix="/user")


@user_router.post(
    "/email/request/verify/code",
    description=f"""
    **[API Description]** <br><br>
    Request verify code for register user and duplicated check of email <br><br>
    **[Exception List]** <br><br> 
    {EMAIL_CONFLICT_SYSTEM_CODE}: 이메일 중복 오류(409)
    """,
)
def email_request_verify_code(
    user_data: EmailVerifySchema, db: Session = Depends(get_db)
):
    email_con.send_verify_code(db, user_data)
    return {"success": True}


@user_router.post(
    "/email/verify/auth/code",
    description=f"""
    **[API Description]** <br><br>
    Verify code(expiration time: 3min) <br><br>
    **[Exception List]** <br><br>
    {EMAIL_AUTH_NUMBER_INVALID_SYSTEM_CODE}: 인증번호 오류(400) <br><br>
    {EMAIL_VERIFY_CODE_EXPIRED_SYSTEM_CODE}: 이메일 인증 만료(400)
    """,
)
def email_verify_auth_code(
    user_data: EmailAuthCodeSchema, db: Session = Depends(get_db)
):
    email_con.verify_auth_code(db, user_data)
    return {"success": True}


@user_router.post(
    "/email/register",
    description=f"""
    **[API Description]** <br><br>
    Verify code(expiration time: 3min) <br><br>
    **[Exception List]** <br><br>
    {PASSWORD_INVALID_SYSTEM_CODE}: 비밀번호 오류(400) <br><br>
    {EMAIL_CONFLICT_SYSTEM_CODE}: 이메일 중복 오류(409)
    """,
    response_model=CreateResponse,
)
def email_register_user(user_data: EmailRegisterSchema, db: Session = Depends(get_db)):
    con.email_register_user(db, user_data)
    return {"success": True}


@user_router.post("/email/login")
def email_login(user_data: EmailLoginSchema, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == user_data.email))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"system_code": "USER_NOT_FOUND"},
        )

    if not user.profile:
        raise ProfileRequired

    result = verify_password(user_data.password, user.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"system_code": "USER_PASSWORD_NOT_MATCHED"},
        )

    access_token = create_access_token(data={"sub": str(user_data.email)})
    refresh_token = create_refresh_token(data={"sub": str(user_data.email)})

    return {"access_token": access_token, "refresh_token": refresh_token}


@user_router.post("/email/request/password/reset")
def email_request_password_reset(
    user_data: EmailPasswordResetSchema, db: Session = Depends(get_db)
):
    email_con.send_verify_code_for_reset_password(db, user_data)
    return {"success": True}


@user_router.post("/password/reset")
def user_reset_password(user_data: ResetPasswordSchema, db: Session = Depends(get_db)):
    con.reset_password(db, user_data)
    return {"success": True}


@user_router.post("/token/refresh")
def get_access_token_using_refresh_token(
    user_data: RefreshTokenSchema,
    db: Session = Depends(get_db),
):
    username = validate_refresh_token(user_data, db)

    access_token = create_access_token(data={"sub": username})
    refresh_token = create_refresh_token(data={"sub": username})

    return {"access_token": access_token, "refresh_token": refresh_token}


@user_router.get("/me", response_model=UserSchema)
def get_user_info_with_profile(
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return token


@user_router.patch("/me")
def update_user_profile(
    user_data: UpdateProfileSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    profile = token.profile[0]
    position = user_data.position

    for key, value in user_data.dict(exclude_none=True).items():
        setattr(profile, key, value)

    if position is not None:
        sql = delete(JoinPosition).where(JoinPosition.profile_seq == profile.seq)
        db.execute(sql)

        obj = [
            JoinPosition(profile_seq=profile.seq, position_seq=item)
            for item in position
        ]
        db.bulk_save_objects(obj)

    db.commit()
    db.flush()
    return {"success": True}
