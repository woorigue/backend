import boto3
from io import BytesIO
from app.model.banner import Banner

from datetime import datetime


class FileController:
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def upload_uesr_profile_img(self, file, user, file_name, db):
        url = f"profile/{user.email}/{file_name}"
        content = BytesIO(file)
        self.s3_client.upload_fileobj(content, "our-league", url)
        profile = user.profile[0]
        profile.img = "drl2968ia795g.cloudfront.net/" + url
        db.commit()
        db.flush()

    def upload_banner_img(self, file, file_name, db):
        url = f"banner/{file_name}"
        content = BytesIO(file)
        self.s3_client.upload_fileobj(content, "our-league", url)
        banner = Banner(
            url="drl2968ia795g.cloudfront.net/" + url, create_date=datetime.now()
        )
        db.add(banner)
        db.commit()
        db.flush()

    def edit_banner_img(self, file, file_name):
        url = f"banner/{file_name}"
        content = BytesIO(file)
        self.s3_client.upload_fileobj(content, "our-league", url)
        return "drl2968ia795g.cloudfront.net/" + url


file_controller = FileController()
