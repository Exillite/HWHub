from fastapi import APIRouter, WebSocket, Depends
from typing import Optional, Dict
import uuid
import json

from . import auth
from .. import schemas
from .. import models

from .. import crud


router = APIRouter(
    prefix="/api/v0.1/call",
    responses={404: {"description": "Not found"}},
    tags=["Call"],
)


class Connection:
    client1: WebSocket
    client1_data = None

    client2: WebSocket
    client2_data = None

    def __init__(self, client) -> None:
        self.client1 = client


class Con:
    id: str
    client_user: schemas.User
    client2_user: Optional[models.UserModel] = None

    free: bool
    group: models.StudentGroupModel

    def __init__(self, id, user, group) -> None:
        self.id = id
        self.client_user = user
        self.free = True
        self.group = group


db: Dict[str, Connection] = {}
cons: Dict[str, Con] = {}


@router.post("/new_call/{student_group_id}/{student_id}")
async def new_call(student_group_id: str, student_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    new_id = str(uuid.uuid4())
    while new_id in db:
        new_id = str(uuid.uuid4())

    student_group = await crud.get_student_group(student_group_id)
    cons[new_id] = Con(id=new_id, user=current_user, group=student_group)
    cons[new_id].client2_user = await crud.get_user(student_id)

    return {"id": new_id}


@router.get("/get_calls")
async def get_call(current_user: schemas.User = Depends(auth.get_current_active_user)):
    calls = []  # type: ignore
    for i in cons:
        calls.append(
            {'id': cons[i].id, 'user': cons[i].client_user.dict(), 'free': cons[i].free})

    return {'calls': calls}


async def call_handler(websocket: WebSocket, cnct_id: str):
    await websocket.accept()
    if cnct_id not in db:
        db[cnct_id] = Connection(websocket)
    else:
        db[cnct_id].client2 = websocket
        # cons[cnct_id].free = False
    while True:
        data = await websocket.receive_text()

        data = json.loads(data)

        if data['type'] == 'new_connection':  # type: ignore
            db[cnct_id].client1_data = json.loads(data['data'])  # type: ignore
        if data['type'] == 'connection_request':  # type: ignore
            rsp = {'type': 'connect_response'}
            rsp['data'] = db[cnct_id].client1_data  # type: ignore
            rsp['title'] = f"{cons[cnct_id].client_user.name} {cons[cnct_id].client_user.surname} - {cons[cnct_id].group.title}"
            if db[cnct_id].client2:
                await db[cnct_id].client2.send_text(json.dumps(rsp))
        if data['type'] == 'connect':  # type: ignore
            db[cnct_id].client2_data = json.loads(data['data'])  # type: ignore

            rsp = {'type': 'connect_final'}
            rsp['data'] = db[cnct_id].client2_data  # type: ignore

            rsp['title'] = \
                f"{cons[cnct_id].client2_user.name} {cons[cnct_id].client2_user.surname} - {cons[cnct_id].group.title}"  # type: ignore
            await db[cnct_id].client1.send_text(json.dumps(rsp))
        if data['type'] == 'get_homeworks':  # type: ignore
            homeworks = await crud.get_homeworks_by_students_group(cons[cnct_id].group)
            rsp = {'type': 'get_homeworks_response'}
            print("!!!!!!!!!!!!!!!", len(homeworks))
            rsp['data'] = [hw.to_json() for hw in homeworks]  # type: ignore
            await db[cnct_id].client1.send_text(json.dumps(rsp))
        if data['type'] == 'get_submisssion':  # type: ignore
            print("?????????????????????3")
            print(data)
            hw = await crud.get_homework(data['homework_id'])  # type: ignore
            usr = cons[cnct_id].client2_user
            if usr and hw:
                submission = await crud.get_submission_by_homework_and_student(hw=hw, user=usr)
            rsp = {'type': 'get_submisssion_response'}
            rsp['data'] = submission.to_json()  # type: ignore
            await db[cnct_id].client1.send_text(json.dumps(rsp))
        if data['type'] == 'edit_submisssion':  # type: ignore
            edit_sub = schemas.SubmissionUpdate(
                points=data['data']['points'], fine=data['data']['fine'])  # type: ignore
            # type: ignore
            await crud.edit_submission(edit_sub, data['submission_id']) # type: ignore
