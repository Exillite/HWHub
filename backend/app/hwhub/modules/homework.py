from fastapi import APIRouter, Depends

from typing import Optional

from .. import crud
from .. import schemas
from .. import validations
from . import auth

router = APIRouter(
    prefix="/api/v0.1/homework",
    responses={404: {"description": "Not found"}},
    tags=["Homework"],
)


async def check_permision(user: schemas.User, homework_id: Optional[str] = None, student_group_id: Optional[str] = None, perm="c") -> bool:
    """
    perm:
    c - create |
    r - read |
    e - edit
    """
    if user.role == "admin":
        return True

    if perm == "c" and student_group_id:
        stg = await crud.get_student_group(student_group_id)
        if stg:
            return user.role in ["teacher"] and user.id == stg.teacher.id
    if perm == "r" and homework_id:
        hw = await crud.get_homework(homework_id)
        if hw:
            if hw.student_group.id:
                stg = await crud.get_student_group(hw.student_group.id)
                if stg:
                    for u_stg in user.students_groups:
                        if stg.id == u_stg.id:
                            return True
                    return stg.teacher.id == user.id
    if perm == "e" and homework_id:
        hw = await crud.get_homework(homework_id)
        if not hw:
            return False
        if not hw.student_group.id:
            return False
        stg = await crud.get_student_group(hw.student_group.id)
        if not stg:
            return False
        return stg.teacher.id == user.id
    return False


@router.post("/")
async def create_new_homework(new_hw: schemas.HomeworkCreate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, student_group_id=new_hw.student_group_id):
        return {"status": 400}
    try:
        hw = await crud.create_homework(new_hw)
        if not hw:
            return {"status": 201}
        return {"status": 200, "homework_id": str(hw.id)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{homework_id}")
async def get_homework(homework_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, homework_id=homework_id, perm="r"):
        return {"status": 400}
    try:
        hw = await crud.get_homework(homework_id)
        if not hw:
            return {"status": 201}
        return {"status": 200, "homework": hw.to_json()}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.put("/{homework_id}")
async def edit_homework(homework_id: str, edit_hw: schemas.HomeworkUpdate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, homework_id=homework_id, perm="e"):
        return {"status": 400}
    try:
        hw = await crud.edit_homework(edit_hw, homework_id)
        if not hw:
            return {"status": 201}
        return {"status": 200, "homework_id": str(hw.id)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.delete("/{homework_id}")
async def delete_homework(homework_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, homework_id=homework_id, perm="e"):
        return {"status": 400}
    try:
        await crud.delete_homework(homework_id)
        return {"status": 200}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{homework_id}/submissions")
async def get_homework_results(homework_id, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, homework_id=homework_id, perm="r"):
        return {"status": 400}
    try:
        hw = await crud.get_homework(homework_id)
        if not hw:
            return {"status": 201}
        subs = [sub.to_json() for sub in await crud.get_submissions_by_homework(hw)]
        return {"status": 200, "submissions": subs}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{homework_id}/marks")
async def get_homework_marks(homework_id, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, homework_id=homework_id, perm="r"):
        return {"status": 400}
    try:
        hw = await crud.get_homework(homework_id)
        if not hw:
            return {"status": 201}
        subs = await crud.get_submissions_by_homework(hw)

        resp = {"users": []}  # type: ignore

        for sub in subs:
            resp["users"].append(
                {"user": f"{sub.student.name} {sub.student.surname} {sub.student.patronymic}"})
            for i in range(len(sub.points)):
                resp["users"][-1][i] = sub.points[i]
            resp["users"][-1]["fine"] = sub.fine
            resp["users"][-1]["mark"] = sub.mark

        return {"status": 200, "marks": resp}
    except Exception as e:
        return {"status": 500, "error": str(e)}
