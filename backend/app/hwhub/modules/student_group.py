from fastapi import APIRouter, Depends

from typing import Optional

from .. import crud
from .. import schemas
from .. import validations
from . import auth

router = APIRouter(
    prefix="/api/v0.1/student_group",
    responses={404: {"description": "Not found"}},
    tags=["Student Group"],
)


async def check_permision(user: schemas.User, student_group_id: Optional[str] = None, perm="c") -> bool:
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
    if perm == "r" and student_group_id:
        stg = await crud.get_student_group(student_group_id)
        if not stg:
            return False

        for u_stg in user.students_groups:
            if stg.id == u_stg.id:
                return True
        return stg.teacher.id == user.id
    if perm == "e" and student_group_id:
        stg = await crud.get_student_group(student_group_id)
        if not stg:
            return False
        return stg.teacher.id == user.id
    return False


@router.post("/")
async def create_new_student_group(new_stg: schemas.StudentGroupCreate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    """
    400 - отказано в доступе
    """
    if not await check_permision(current_user):
        return {"status": 400}

    try:
        stg = await crud.create_student_group(new_stg)
        if not stg:
            return {"status": 201}
        return {"status": 200, "student_group_id": str(stg.id)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{student_group_id}")
async def get_student_group(student_group_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, student_group_id, perm="r"):
        return {"status": 400}
    # try:
    stg = await crud.get_student_group(student_group_id)
    if not stg:
        return {"status": 201}
    return {"status": 200, "student_group": stg.to_json()}
    # except Exception as e:
    #     return {"status": 500, "error": str(e)}


@router.put("/{student_group_id}")
async def edit_student_group(student_group_id: str, edit_stg: schemas.StudentGroupUpdate, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, student_group_id, perm="e"):
        return {"status": 400}
    try:
        stg = await crud.edit_student_group(edit_stg, student_group_id)
        if not stg:
            return {"status": 201}
        return {"status": 200, "student_group": str(stg.id)}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.delete("/{student_group_id}")
async def delete_student_group(student_group_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, student_group_id, perm="e"):
        return {"status": 400}
    try:
        await crud.delete_student_group(student_group_id)
        return {"status": 200}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{student_group_id}/homeworks")
async def get_all_homeworks_from_student_group(student_group_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, student_group_id, perm="r"):
        return {"status": 400}
    try:
        stg = await crud.get_student_group(student_group_id)
        if not stg:
            return {"status": 201}
        homeworks = await crud.get_homeworks_by_students_group(stg)
        return {"status": 200, "homeworks": [hw.to_json() for hw in homeworks]}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{student_group_id}/students")
async def get_student_groups_students(student_group_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, student_group_id, perm="r"):
        return {"status": 400}
    try:
        stdg = await crud.get_student_group(student_group_id)
        if not stdg:
            return {"status": 201}
        students = await crud.get_students_from_students_group(stdg)
        return {"status": 200, "users": [std.to_json() for std in students]}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{student_group_id}/consultants")
async def get_student_groups_consultants(student_group_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, student_group_id, perm="r"):
        return {"status": 400}
    try:
        stdg = await crud.get_student_group(student_group_id)
        if not stdg:
            return {"status": 201}
        students = await crud.get_consultants_from_students_group(stdg)
        return {"status": 200, "users": [std.to_json() for std in students]}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.patch("/{student_group_id}/kick_user/{user_id}")
async def kick_user_from_students_group(student_group_id: str, user_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, student_group_id, perm="e"):
        return {"status": 400}
    try:
        await crud.remove_user_from_student_group(student_group_id, user_id)
        return {"status": 200}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{student_group_id}/get_results")
async def get_results(student_group_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, student_group_id, perm="r"):
        return {"status": 400}
    try:
        stg = await crud.get_student_group(student_group_id)
        if not stg:
            return {"status": 201}
        stds = await crud.get_students_from_students_group(stg)
        students = [st.to_json() for st in stds]

        for i in range(len(students)):
            students[i]['submissions'] = [sub.to_json()
                                          for sub in await crud.get_submissions_by_student(stds[i])]

        return {"status": 200, "users": students}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.get("/{student_group_id}/get_marks")
async def get_marks(student_group_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    if not await check_permision(current_user, student_group_id, perm="r"):
        return {"status": 400}
    try:
        stg = await crud.get_student_group(student_group_id)
        if not stg:
            return {"status": 201}

        stds = await crud.get_students_from_students_group(stg)
        hws = await crud.get_homeworks_by_students_group(stg)

        resp = {'items': []}  # type: ignore

        for std in stds:
            resp['items'].append(
                {'user': f"{std.name} {std.surname} {std.patronymic}"})

            for hw in hws:
                submission = await crud.get_submission_by_homework_and_student(hw, std)
                if submission:
                    resp['items'][-1][hw.id] = submission.mark

        return {"status": 200, "marks": resp}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@router.patch("/{student_group_id}/add_user/{user_id}")
async def add_user_to_students_group(student_group_id: str, user_id: str, current_user: schemas.User = Depends(auth.get_current_active_user)):
    try:
        await crud.add_user_to_student_group(student_group_id, user_id)
        return {"status": 200}
    except Exception as e:
        return {"status": 500, "error": str(e)}
