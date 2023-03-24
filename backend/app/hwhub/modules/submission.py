from fastapi import APIRouter, Depends

from .. import crud
from .. import schemas
from .. import validations
from . import auth

router = APIRouter(
    prefix="/api/v0.1/submission",
    responses={404: {"description": "Not found"}},
    tags=["Submission"],
)

def check_permision(user: schemas.User, submission_id: str = None, homework_id: str = None, perm="c") -> bool:
    """
    perm:
    c - create |
    r - read |
    e - edit
    """
    if user.role == "admin":
        return True
    
    if perm == "c":
        hw = crud.get_homework(homework_id)
        stg = crud.get_student_group(hw.student_group.pk)
        if user.role not in ["teacher", "consultant"]:
            return False
        for u_stg in user.students_groups:
            if stg.pk == u_stg.pk:
                return True
        return user.pk == stg.teacher.pk
    if perm == "r":
        sub = crud.get_submission(submission_id)
        hw = crud.get_homework(sub.homework.pk)
        stg = crud.get_student_group(hw.student_group.pk)
        for u_stg in user.students_groups:
            if stg.pk == u_stg.pk:
                return True
        return stg.teacher.pk == user.pk
    if perm == "e":
        sub = crud.get_submission(submission_id)
        hw = crud.get_homework(sub.homework.pk)
        stg = crud.get_student_group(hw.student_group.pk)
        return stg.teacher.pk == user.pk
    return False


@router.post("/")
def create_new_submission(new_sub: schemas.SubmissionCreate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, homework_id=new_sub.homework_id):
        return {"status": 400}
    try:
        sub = crud.create_submission(new_sub)
        if not sub:
            return {"status": 201}
        return {"status": 200, "submission_id": str(sub.pk)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{submission_id}")
def get_submission(submission_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, submission_id=submission_id, perm="r"):
        return {"status": 400}
    try:
        sub = crud.get_submission(submission_id)
        if not sub:
            return {"status": 201}
        return {"status": 200, "submission": sub.to_json()}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.put("/{submission_id}")
def edit_submission(submission_id: str, edit_sub: schemas.SubmissionUpdate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, submission_id=submission_id, perm="e"):
        return {"status": 400}
    try:
        sub = crud.edit_submission(edit_sub, submission_id)
        if not sub:
            return {"status": 201}
        return {"status": 200, "submission_id": str(sub.pk)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.delete("/{submission_id}")
def delete_submission(submission_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not check_permision(current_user, submission_id=submission_id, perm="e"):
        return {"status": 400}
    try:
        crud.delete_submission(submission_id)
        return {"status": 200}
    except Exception as e:
        return {"status": 500, "error": str(e)}
