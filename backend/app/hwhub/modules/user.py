from fastapi import APIRouter, Depends

from .. import crud
from .. import schemas
from .. import validations
from . import auth

router = APIRouter(
    prefix="/api/v0.1/user",
    responses={404: {"description": "Not found"}},
    tags=["User"],
)

@router.post("/")
async def registaration_new_user(user: schemas.UserCreate):
    try:
        is_valid, status_code = validations.validation_create_user(user)
        if not is_valid:
            return {"status": status_code}

        pwd = str(user.password)
        user.password = auth.get_password_hash(pwd)
        new_user = crud.create_user(user)
        return {"status": status_code, "user_id": str(new_user.pk)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{user_id}")
async def get_user(user_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
        500 - server error
        
        200 - OK
        
        201 - user does not exist
    """
    try:
        user = crud.get_user(user_id)
        if not user:
            return {"status": 201}
        return {"status": 200, "user": user.to_json()}
    except Exception as e:
        return {"status": 500, "error": str(e)}
    

@router.put("/{user_id}")
async def edit_user(user_id: str, edit_user: schemas.UserUpdate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
    400 - отказано в доступе
    """
    if not (user_id == current_user.id or current_user.role == 'admin'):
        return {"status": 400}
    try:
        user = crud.edit_user(edit_user, user_id)
        if not user:
            return {"status": 201} # хз ошибка значит какая то
        return {"status": 200, "user_id": str(user.pk)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
    400 - отказано в доступе
    """
    if not (user_id == current_user.pk or current_user.role == 'admin'):
        return {"status": 400}
    try:
        crud.delete_user(user_id)
        return {"status": 200}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{user_id}/student_groups")
async def get_all_users_stdents_groups(user_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    try:
        user = crud.get_user(user_id)
        students_groups_where_teacher = crud.get_students_group_by_teacher(user_id)
        students_groups = [g.to_json() for g in (user.students_groups or [])] + [g.to_json() for g in students_groups_where_teacher]
        return {"status": 200, "student_groups": students_groups}
    except Exception as e:
        return {"status": 500, "error": str(e)}