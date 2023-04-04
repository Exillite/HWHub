from fastapi import APIRouter, Depends

from .. import crud
from .. import schemas
from .. import validations
from . import auth

router = APIRouter(
    prefix="/api/v0.1/homework",
    responses={404: {"description": "Not found"}},
    tags=["Homework"],
)

def check_permision(user: schemas.User, homework_id: str = None, student_group_id: str = None, perm="c") -> bool:
    """
    perm:
    c - create |
    r - read |
    e - edit
    """
    if user.role == "admin":
        return True
    
    if perm == "c":
        stg = crud.get_student_group(student_group_id)
        return user.role in ["teacher"] and user.pk == stg.teacher.pk
    if perm == "r":
        hw = crud.get_homework(homework_id)
        stg = crud.get_student_group(hw.student_group.pk)
        for u_stg in user.students_groups:
            if stg.pk == u_stg.pk:
                return True
        return stg.teacher.pk == user.pk
    if perm == "e":
        hw = crud.get_homework(homework_id)
        stg = crud.get_student_group(hw.student_group.pk)
        return stg.teacher.pk == user.pk
    return False


@router.post("/")
async def create_new_homework(new_hw: schemas.HomeworkCreate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, student_group_id=new_hw.student_group_id):
        return {"status": 400}
    try:
        hw = crud.create_homework(new_hw)
        if not hw:
            return {"status": 201}
        return {"status": 200, "homework_id": str(hw.pk)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{homework_id}")
async def get_homework(homework_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, homework_id=homework_id, perm="r"):
        return {"status": 400}
    try:
        hw = crud.get_homework(homework_id)
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
        hw = crud.edit_homework(edit_hw, homework_id)
        if not hw:
            return {"status": 201}
        return {"status": 200, "homework_id": str(hw.pk)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.delete("/{homework_id}")
async def delete_homework(homework_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, homework_id=homework_id, perm="e"):
        return {"status": 400}
    try:
        crud.delete_homework(homework_id)
        return {"status": 200}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{homework_id}/results")
async def get_homework_results(homework_id, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, homework_id=homework_id, perm="r"):
        return {"status": 400}
    try:
        subs = [sub.to_json() for sub in crud.get_submissions_by_homework()]
        return {"status": 200, "submissions": subs}
    except Exception as e:
        return {"status": 500, "error": str(e)}
