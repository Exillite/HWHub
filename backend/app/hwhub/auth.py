from app.models import *
from app.schemas import *

import uuid
import datetime

def get_session_token(user: UserModel) -> str:
    # delete old sessions and return session token if exist or create new session and return token

    SessionModel.objects(user=user, created_date__lt=datetime.datetime.now() - datetime.timedelta(days=30)).delete()

    ses = SessionModel.objects(user=user).order_by("-created_date").first()
    if ses:
        return ses.token
    else:
        ses = SessionModel(user=user, token=str(uuid.uuid4())).save()
        return ses.token

def check_auth(token: str) -> User:
    # check is session token correct and return user if correct or None if not
    ses = SessionModel.objects(token=token).first()
    if ses:
        return ses.user
    return None
