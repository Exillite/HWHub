from fastapi import APIRouter, WebSocket, Depends
from typing import Optional, Dict
import uuid
import json

from . import auth
from .. import schemas
from .. import models


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
    client_user: models.UserModel
    free: bool

    def __init__(self, id, user) -> None:
        self.id = id
        self.client_user = user
        self.free = True


db: Dict[str, Connection] = {}
cons: Dict[str, Con] = {}


@router.post("/new_call")
async def new_call(current_user: schemas.User = Depends(auth.get_current_active_user)):
    new_id = str(uuid.uuid4())
    while new_id in db:
        new_id = str(uuid.uuid4())

    cons[new_id] = Con(id=new_id, user=current_user)
    return {"id": new_id}


@router.get("/get_calls")
async def get_call(current_user: schemas.User = Depends(auth.get_current_active_user)):
    calls = []  # type: ignore
    for i in cons:
        calls.append(
            {'id': cons[i].id, 'user': cons[i].client_user.to_json(), 'free': cons[i].free})

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
            if db[cnct_id].client2:
                await db[cnct_id].client2.send_text(json.dumps(rsp))
        if data['type'] == 'connect':  # type: ignore
            db[cnct_id].client2_data = json.loads(data['data'])  # type: ignore

            rsp = {'type': 'connect_final'}
            rsp['data'] = db[cnct_id].client2_data  # type: ignore
            await db[cnct_id].client1.send_text(json.dumps(rsp))
