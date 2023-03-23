from fastapi import APIRouter, Depends

from .. import crud
from .. import schemas
from .. import validations
from . import auth

router = APIRouter(
    prefix="/api/v0.1/student_group",
    responses={404: {"description": "Not found"}},
    tags=["Student Group"],
)

def check_permision(user: schemas.User, student_group_id: str = None, perm="c") -> bool:
    """
    perm:
    c - create new |
    r - read |
    e - edit
    """
    if user.role == "admin":
        return True
    
    if perm == "c":
        return user.role in ["teacher"]
    if perm == "r":
        stg = crud.get_student_group(student_group_id)
        for u_stg in user.students_groups:
            if stg.pk == u_stg.pk:
                return True
        return stg.teacher.pk == user.pk
    if perm == "e":
        stg = crud.get_student_group(student_group_id)
        return stg.teacher.pk == user.pk
    return False


@router.post("/")
def create_new_student_group(new_stg: schemas.StudentGroupCreate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
    400 - отказано в доступе
    """
    if not check_permision(current_user):
        return {"status": 400}
    
    try:
        stg = crud.create_student_group(new_stg)
        if not stg:
            return {"status": 201}
        return {"status": 200, "student_group_id": str(stg.pk)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{student_group_id}")
def get_student_group(student_group_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, student_group_id, perm="r"):
        return {"status": 400}
    try:
        stg = crud.get_student_group(student_group_id)
        if not stg:
            return {"status": 201}
        return {"status": 200, "student_group": stg.to_json()}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.put("/{student_group_id}")
def edit_student_group(student_group_id: str, edit_stg: schemas.StudentGroupUpdate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, student_group_id, perm="e"):
        return {"status": 400}
    try:
        stg = crud.edit_student_group(edit_stg, student_group_id)
        if not stg:
            return {"status": 201}
        return {"status": 200, "student_group": str(stg.pk)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.delete("/{student_group_id}")
def delete_student_group(student_group_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, student_group_id, perm="e"):
        return {"status": 400}
    try:
        crud.delete_student_group(student_group_id)
        return {"status": 200}
    except Exception as e:
        return {"status": 500, "error": str(e)}
