from sqlalchemy.orm import Session

from app.model.user import User
from app.model.profile import Profile
from app.model.sns import Sns

from app.rest_api.schema.user import EmailRegisterSchema, ResetPasswordSchema, SnsRegisterSchema


class UserController:
    def email_register_user(self, db: Session, user_data: EmailRegisterSchema):
        
        user = User.create(db, email=user_data.email, password=user_data.password)
        profile = Profile.create(db, user_seq=user.seq, nickname=user_data.nickname)
        
        return user
    
    def sns_register_user(self, db: Session, sns_data: SnsRegisterSchema):

        sns = Sns.create(db, user_seq=sns_data.user_seq, type=sns_data.type, user=sns_data.user)
        
        return sns

    def reset_password(self, db: Session, user_data: ResetPasswordSchema) -> None:
        User.resset_password(db, email=user_data.email, password=user_data.password)
    
    

user_controller = UserController()
