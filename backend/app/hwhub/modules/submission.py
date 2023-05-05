from fastapi import APIRouter, Depends

from typing import Optional

from .. import crud
from .. import schemas
from .. import validations
from . import auth

router = APIRouter(
    prefix="/api/v0.1/submission",
    responses={404: {"description": "Not found"}},
    tags=["Submission"],
)


async def check_permision(user: schemas.User, submission_id: Optional[str] = None, homework_id: Optional[str] = None, perm="c") -> bool:
    """
    perm:
    c - create |
    r - read |
    e - edit
    """
    if user.role == "admin":
        return True

    if perm == "c" and homework_id:
        hw = await crud.get_homework(homework_id)
        if not hw:
            return False
        if not hw.student_group.id:
            return False
        stg = await crud.get_student_group(hw.student_group.id)
        if not stg:
            return False
        if user.role not in ["teacher", "consultant"]:
            return False
        for u_stg in user.students_groups:
            if stg.id == u_stg.id:
                return True
        return user.id == stg.teacher.id
    if perm == "r" and submission_id:
        sub = await crud.get_submission(submission_id)
        if not sub:
            return False
        if not sub.homework.id:
            return False
        hw = await crud.get_homework(sub.homework.id)
        if not hw:
            return False
        if not hw.student_group.id:
            return False
        stg = await crud.get_student_group(hw.student_group.id)
        if not stg:
            return False
        for u_stg in user.students_groups:
            if stg.id == u_stg.id:
                return True
        return stg.teacher.id == user.id
    if perm == "e" and submission_id:
        sub = await crud.get_submission(submission_id)
        if not sub:
            return False
        if not sub.homework.id:
            return False
        hw = await crud.get_homework(sub.homework.id)
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
async def create_new_submission(new_sub: schemas.SubmissionCreate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, homework_id=new_sub.homework_id):
        return {"status": 400}
    try:
        sub = await crud.create_submission(new_sub)
        if not sub:
            return {"status": 201}
        return {"status": 200, "submission_id": str(sub.id)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{submission_id}")
async def get_submission(submission_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, submission_id=submission_id, perm="r"):
        return {"status": 400}
    try:
        sub = await crud.get_submission(submission_id)
        if not sub:
            return {"status": 201}
        return {"status": 200, "submission": sub.to_json()}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.put("/{submission_id}")
async def edit_submission(submission_id: str, edit_sub: schemas.SubmissionUpdate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, submission_id=submission_id, perm="e"):
        return {"status": 400}
    try:
        sub = await crud.edit_submission(edit_sub, submission_id)
        if not sub:
            return {"status": 201}
        return {"status": 200, "submission_id": str(sub.id)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.delete("/{submission_id}")
async def delete_submission(submission_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, submission_id=submission_id, perm="e"):
        return {"status": 400}
    try:
        await crud.delete_submission(submission_id)
        return {"status": 200}
    except Exception as e:
        return {"status": 500, "error": str(e)}
