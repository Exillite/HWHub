from fastapi import APIRouter, WebSocket, Depends
from typing import Optional, List, Set
import uuid


from . import auth
from .. import schemas
from .. import models

from .. import crud


class Position:
    id: str
    student: models.UserModel
    group: models.StudentGroupModel

    def __init__(self, student: models.UserModel, group: models.StudentGroupModel):
        self.id = str(uuid.uuid4())
        self.student = student
        self.group = group


router = APIRouter(
    prefix="/api/v0.1/queue",
    responses={404: {"description": "Not found"}},
    tags=["Queue"],
)


Consultants: List[models.UserModel] = []
Q: List[Position] = []


def queue_response(queue: List[Position]):
    response = []
    for position in queue:
        response.append({
            "id": position.id,
            "student": position.student.to_json(),
            "group": position.group.to_json()
        })
    return response


def add_student(position: Position) -> bool:
    for pos in Q:
        if pos.student.id == position.student.id:
            return False
    Q.append(position)
    return True


def remove_student(position_id: str):
    for i in range(len(Q)):
        if Q[i].id == position_id:
            Q.pop(i)
            return


def add_consultant(consultant: models.UserModel):
    Consultants.append(consultant)


def remove_consultant(consultant: models.UserModel):
    Consultants.remove(consultant)


def get_student(position_id: str) -> Optional[Position]:
    for i in range(len(Q)):
        if Q[i].id == position_id:
            return Q[i]
    return None


def get_queue_for_consultant(consultant: models.UserModel) -> List[Position]:
    queue: List[Position] = []
    for position in Q:
        if position.group in consultant.students_groups:
            queue.append(position)
    return queue


def get_queue_for_position(student_position: Position) -> List[Position]:
    groups: Set[models.StudentGroupModel] = set()
    queue: List[Position] = []

    for consultant in Consultants:
        if student_position.group in consultant.students_groups:
            groups.add(student_position.group)

    for position in Q:
        if position.group in groups:
            queue.append(position)

    return queue


@router.patch("/add_student/{student_group_id}")
async def add_student_endpoint(student_group_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    user = await crud.get_user(current_user.id)
    student_group = await crud.get_student_group(student_group_id)
    if not user or not student_group:
        return {"status": 400}
    position = Position(user, student_group)
    if add_student(position):
        return {"status": 200}
    else:
        return {"status": 400}


@router.patch("/add_consultant")
async def add_consultant_endpoint(current_user: schemas.User = Depends(auth.get_current_active_user)):
    user = await crud.get_user(current_user.id)
    if not user:
        return {"status": 400}
    Consultants.append(user)
    return {"status": 200}


@router.get("/get_queue")
async def get_queue(current_user: schemas.User = Depends(auth.get_current_active_user)):
    if current_user.role == "student":
        current_position = None
        for pos in Q:
            if pos.student.id == current_user.id:
                current_position = pos
                break
        if not current_position:
            return {"status": 400}

        current_queue = get_queue_for_position(current_position)
        return {"status": 200, "queue": queue_response(current_queue)}
    if current_user.role == "consultant":
        consultant = await crud.get_user(current_user.id)
        if not consultant:
            return {"status": 400}
        current_queue = get_queue_for_consultant(consultant)
        return {"status": 200, "queue": queue_response(current_queue)}
