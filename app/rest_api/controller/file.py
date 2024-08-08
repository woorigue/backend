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
        self.s3_client.upload_fileobj(content, "woorigue", url)
        profile = user.profile[0]
        profile.img = "d2al7pp3zcl1yf.cloudfront.net/" + url
        db.commit()
        db.flush()

    def upload_banner_img(self, file, file_name, db):
        url = f"banner/{file_name}"
        content = BytesIO(file)
        self.s3_client.upload_fileobj(content, "woorigue", url)
        banner = Banner(
            url="d2al7pp3zcl1yf.cloudfront.net/" + url, create_date=datetime.now()
        )
        db.add(banner)
        db.commit()
        db.flush()

    def edit_banner_img(self, file, file_name):
        url = f"banner/{file_name}"
        content = BytesIO(file)
        self.s3_client.upload_fileobj(content, "woorigue", url)
        return "d2al7pp3zcl1yf.cloudfront.net/" + url

    def upload_club_img(self, file, file_name):
        url = f"club/{file_name}"
        content = BytesIO(file)
        self.s3_client.upload_fileobj(content, "woorigue", url)
        return "d2al7pp3zcl1yf.cloudfront.net/" + url

    def upload_club_emblem_img(self, file, file_name):
        url = f"club/emblem/{file_name}"
        content = BytesIO(file)
        self.s3_client.upload_fileobj(content, "woorigue", url)
        return "d2al7pp3zcl1yf.cloudfront.net/" + url


file_controller = FileController()
