# __**API Documentation**__

# __Objects__

---
### User
- id - unique identifier primary key
- login (string) - unique
- role (string) - role of user ("student" | "consultant", "teacher" | "admin" | "user")
- name (string) - first name
- surname (string)  - last name
- patronymic (string) - middle name
- email (string) - email
- vk_id (int) - vk id (optional)
- telegram_id (int) - telegram id (optional)
- is_active (bool) - is user active

Example:
```json
{
    "id": "123456",
    "login": "johndoe",
    "role": "student",
    "name": "John",
    "surname": "Doe",
    "patronymic": "W.",
    "email": "johndoe@example.com",
    "vk_id": 123456789,
    "telegram_id": 987654321,
    "is_active": true,
}
```

### StudentGroup
- id - unique identifier primary key
- title (string) - title of group
- teacher (User) - teacher of group
- connect_code (string) - code for connecting to group
- is_active (bool) - is group active

Example:
```json
{
    "id": "123456",
    "title": "Computer Science 101",
    "teacher": {
        "id": "789012",
        "login": "janedoe",
        "role": "teacher",
        "name": "Jane",
        "surname": "Doe",
        "patronymic": "R.",
        "email": "janedoe@example.com",
        "vk_id": null,
        "telegram_id": null,
        "is_active": true
    },
    "connect_code": "abc123",
    "is_active": true
}
```

### Homework
- id - unique identifier primary key
- title (string) - title of homework
- files (array of URLs) - link to file
- student_group (StudentGroup) - student group
- uploaded_at (datetime) - date and time of upload
- deadline (datetime) - deadline date and time
- last_updated_at (datetime) - date and time of last update
- points (array of double) - points for each task
- mark_formula (string) - formula for calculating mark
- is_active (bool) - is homework active

Example:
```json
{
    "id": "123456",
    "title": "Programming Assignment 1",
    "file": "https://example.com/programming-assignment-1.pdf",
    "student_group": {
        "id": "654321",
        "title": "Computer Science 101",
        "teacher": {
            "id": "789012",
            "login": "janedoe",
            "role": "teacher",
            "name": "Jane",
            "surname": "Doe",
            "patronymic": "R.",
            "email": "janedoe@example.com",
            "vk_id": null,
            "telegram_id": null,
            "is_active": true
        },
        "connect_code": "abc123",
        "is_active": true
    },
    "uploaded_at": "2023-04-02T10:00:00Z",
    "deadline": "2023-04-09T10:00:00Z",
    "last_updated_at": "2023-04-03T15:30:00Z",
    "points": [7.5, 5.0, 2.5],
    "mark_formula": "(K + 3) / 10",
    "is_active": true,
}
```

### Submission
- id - unique identifier primary key
- student (User) - student
- homework (Homework) - homework
- points (array of double) - length of array must be equal to length of points array in homework, each element is 1 if task is done, 0 otherwise or percentage of task completion (for example, 0.5 if task is done half)
- fine (double) - fine for late submission (0 if submitted on time)
- mark (double) - mark for submission, calculated by formula in homework
- start_submit (datetime) - date and time of start of submission
- last_updated_at (datetime) - date and time of last update
- is_active (bool) - is submission active

Example:
```json
{
    "id": 987654,
    "student": {
        "id": "654321",
        "login": "johnsmith",
        "role": "student",
        "name": "John",
        "surname": "Smith",
        "patronymic": "W.",
        "email": "johnsmith@example.com",
        "vk_id": "123456",
        "telegram_id": null,
        "is_active": true
    },
    "homework": {
        "id": "123456",
        "title": "Programming Assignment 1",
        "file": "https://example.com/programming-assignment-1.pdf",
        "student_group": {
            "id": "654321",
            "title": "Computer Science 101",
            "teacher": {
                "id": 789012,
                "login": "janedoe",
                "role": "teacher",
                "name": "Jane",
                "surname": "Doe",
                "patronymic": "R.",
                "email": "janedoe@example.com",
                "vk_id": null,
                "telegram_id": null,
                "is_active": true
            },
            "connect_code": "abc123",
            "is_active": true
        },
        "uploaded_at": "2023-04-02T10:00:00Z",
        "deadline": "2023-04-09T10:00:00Z",
        "last_updated_at": "2023-04-03T15:30:00Z",
        "points": [7.5, 5.0, 2.5],
        "mark_formula": "K - 3",
        "is_active": true
    },
    "points": [1.0, 0.5, 0.0],
    "fine": 0.0,
    "mark": 4.0,
    "start_submit": "2023-04-08T08:00:00Z",
    "last_updated_at": "2023-04-09T09:00:00Z",
    "is_active": true
}

```

# __Methods__
---

## **Main**

### Get My Accaunt
- URL: `/api/v0.1/me`
- method: **GET**
- auth required: **YES**
- response body:
```json
{
    "status": int,
    "user": {
        "id": str,
        "login": str,
        "role": str,
        "name": str,
        "surname": str,
        "patronymic": str,
        "email": str,
        "vk_id": int,
        "telegram_id": int,
        "is_active": bool,
    }
}
```
- status codes:
  - 200 - OK
  - 400 - Permission denied
  - 500 - Server error

## **Auth**

### Get My Accaunt
- URL: `/api/v0.1/auth/token`
- method: **POST**
- auth required: **NO**
- description: Return token, which your need to save on client side.
- request body:
```json
{
    "username": str,
    "password": str,
}
```
- response body:
```json
{
    "access_token": "string",
    "token_type": "string"
}
```

## **User**

### Create New User
- URL: `/api/v0.1/user/`
- method: **POST**
- auth required: **NO**
- description: 
- request body:
```json
{
    "login": str,
    "name": str,
    "surname": str,
    "patronymic": str,
    "email": str,
    "password": str,
}
```
- response body:
```json
{
    "status": int,
    "user_id": str,
}
```
- status codes:
  - 200 - OK
  - 202 - User email is invalid or already exists.
  - 203 - User password is invalid.
  - 204 - User with this login already exists.
  - 400 - Permission denied
  - 500 - Server error

### Get User
- URL: `/api/v0.1/user/{user_id}`
- method: **GET**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
    "user": {
        "id": str,
        "login": str,
        "role": str,
        "name": str,
        "surname": str,
        "patronymic": str,
        "email": str,
        "vk_id": int,
        "telegram_id": int,
        "is_active": bool,
    },
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Edit User
- URL: `/api/v0.1/user/{user_id}`
- method: **PUT**
- auth required: **YES**
- description: 
- request body:
```json
{
    "name": str,
    "surname": str,
    "patronymic": str,
}
```
- response body:
```json
{
    "status": int,
    "user_id": str,
}
```
- status codes:
  - 200 - OK
  - 400 - Permission denied
  - 500 - Server error

### Delete User
- URL: `/api/v0.1/user/{user_id}`
- method: **DELETE**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Get All User`s Student Groups
- URL: `/api/v0.1/user/{user_id}/student_groups`
- method: **GET**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
    "student_groups": [
        {
            "id": str,
            "title": str,
            "teacher": {
                "id": str,
                "login": str,
                "role": str,
                "name": str,
                "surname": str,
                "patronymic": str,
                "email": str,
                "vk_id": int,
                "telegram_id": int,
                "is_active": bool,
            },
            "connect_code": str,
            "is_active": bool,
        }
    ],
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error


## **Student Group**

### Create Student Group
- URL: `/api/v0.1/student_group/`
- method: **POST**
- auth required: **YES**
- description: 
- request body:
```json
{
    "title": str,
    "teacher_id": str,
}
```
- response body:
```json
{
    "status": int,
    "student_group_id": str,
}
```
- status codes:
  - 200 - OK
  - 400 - Permission denied
  - 500 - Server error

### Get Student Group
- URL: `/api/v0.1/student_group/{student_group_id}`
- method: **GET**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
    "student_group": {
        "id": str,
        "title": str,
        "teacher": {
            "id": str,
            "login": str,
            "role": str,
            "name": str,
            "surname": str,
            "patronymic": str,
            "email": str,
            "vk_id": int,
            "telegram_id": int,
            "is_active": bool,
        },
        "connect_code": str,
        "is_active": bool,
    },
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Edit Student Group
- URL: `/api/v0.1/student_group/{student_group_id}`
- method: **PUT**
- auth required: **YES**
- description: 
- request body:
```json
{
    "title": str,
}
```
- response body:
```json
{
    "status": int,
    "student_group_id": str,
}
```
- status codes:
  - 200 - OK
  - 400 - Permission denied
  - 500 - Server error

### Delete Student Group
- URL: `/api/v0.1/student_group/{student_group_id}`
- method: **DELETE**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Get Homeworks from Student Group
- URL: `/api/v0.1/student_group/{student_group_id}/homeworks`
- method: **GET**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
    "homeworks": [
        {
            "id": str,
            "title": str,
            "file": str,
            "student_group": {
                "id": str,
                "title": str,
                "teacher": {
                    "id": str,
                    "login": str,
                    "role": str,
                    "name": str,
                    "surname": str,
                    "patronymic": str,
                    "email": str,
                    "vk_id": int,
                    "telegram_id": int,
                    "is_active": bool,
                },
                "connect_code": str,
                "is_active": bool,
            },
            "uploaded_at": datetime,
            "deadline": datetime,
            "last_updated_at": datetime,
            "points": [float],
            "mark_formula": str,
            "is_active": bool,
        }
    ],
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Get Students from Student Group
- URL: `/api/v0.1/student_group/{student_group_id}/students`
- method: **GET**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
    "users": [
        {
            "id": str,
            "login": str,
            "role": str,
            "name": str,
            "surname": str,
            "patronymic": str,
            "email": str,
            "vk_id": int,
            "telegram_id": int,
            "is_active": bool,
        }
    ],
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Get Consultants from Student Group
- URL: `/api/v0.1/student_group/{student_group_id}/consultants`
- method: **GET**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
    "users": [
        {
            "id": str,
            "login": str,
            "role": str,
            "name": str,
            "surname": str,
            "patronymic": str,
            "email": str,
            "vk_id": int,
            "telegram_id": int,
            "is_active": bool,
        }
    ],
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Kick User from Student Group
- URL: `/api/v0.1/student_group/{student_group_id}/kick/{user_id}`
- method: **PATCH**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Get Student Group`s results
- URL: `/api/v0.1/student_group/{student_group_id}/get_results`
- method: **GET**
- auth required: **YES**
- description: Return students list with additional param 'submissions'.
- response body:
```json
{
    "status": int,
    "users": [
        {
            "id": str,
            "login": str,
            "role": str,
            "name": str,
            "surname": str,
            "patronymic": str,
            "email": str,
            "vk_id": int,
            "telegram_id": int,
            "is_active": bool,

            "submissions": [
                {
                    {
                        "id": str,
                        "student": {
                            "id": str,
                            "login": str,
                            "role": str,
                            "name": str,
                            "surname": str,
                            "patronymic": str,
                            "email": str,
                            "vk_id": int,
                            "telegram_id": int,
                            "is_active": bool,
                        },
                        "homework": {
                            "id": str,
                            "title": str,
                            "file": URL,
                            "student_group": {
                                "id": str,
                                "title": str,
                                "teacher": {
                                    "id": str,
                                    "login": str,
                                    "role": str,
                                    "name": str,
                                    "surname": str,
                                    "patronymic": str,
                                    "email": str,
                                    "vk_id": int,
                                    "telegram_id": int,
                                    "is_active": int,
                                },
                                "connect_code": str,
                                "is_active": bool,
                            },
                            "uploaded_at": datetime,
                            "deadline": datetime,
                            "last_updated_at": datetime,
                            "points": [float],
                            "mark_formula": str,
                            "is_active": bool,
                        },
                        "points": [float],
                        "fine": float,
                        "mark": float,
                        "start_submit": datetime,
                        "last_updated_at": datetime,
                        "is_active": bool,
                    }
                }
            ]
        }
    ],
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error


## **Homework**

### Create Homework
- URL: `/api/v0.1/homework/`
- method: **POST**
- auth required: **YES**
- description: 
- request body:
```json
{
    "title": str,
    "file": URL,
    "student_group_id": str,
    "deadline": datetime.datetime,
    "points": [float],
    "mark_formula": str,
}
```
- response body:
```json
{
    "status": int,
    "homework_id": str,
}
```
- status codes:
  - 200 - OK
  - 400 - Permission denied
  - 500 - Server error

### Get Homework
- URL: `/api/v0.1/homework/{homework_id}`
- method: **GET**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
    "homework": {
        "id": str,
        "title": str,
        "file": URL,
        "student_group": {
            "id": str,
            "title": str,
            "teacher": {
                "id": str,
                "login": str,
                "role": str,
                "name": str,
                "surname": str,
                "patronymic": str,
                "email": str,
                "vk_id": int,
                "telegram_id": int,
                "is_active": int,
            },
            "connect_code": str,
            "is_active": bool,
        },
        "uploaded_at": datetime,
        "deadline": datetime,
        "last_updated_at": datetime,
        "points": [float],
        "mark_formula": str,
        "is_active": bool,
    },
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Edit Homework
- URL: `/api/v0.1/homework/{homework_id}`
- method: **PUT**
- auth required: **YES**
- description: 
- request body:
```json
{
    "title": str,
    "file": str,
    "deadline": datatime,
    "points": [float],
    "mark_formula": str,
}
```
- response body:
```json
{
    "status": int,
    "homework_id": str,
}
```
- status codes:
  - 200 - OK
  - 400 - Permission denied
  - 500 - Server error

### Delete Homework
- URL: `/api/v0.1/homework/{homework_id}`
- method: **DELETE**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Get Homework`s Results
- URL: `/api/v0.1/homework/{homework_id}/submissions`
- method: **GET**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
    "submissions": [
        {
            {
                "id": str,
                "student": {
                    "id": str,
                    "login": str,
                    "role": str,
                    "name": str,
                    "surname": str,
                    "patronymic": str,
                    "email": str,
                    "vk_id": int,
                    "telegram_id": int,
                    "is_active": bool,
                },
                "homework": {
                    "id": str,
                    "title": str,
                    "file": URL,
                    "student_group": {
                        "id": str,
                        "title": str,
                        "teacher": {
                            "id": str,
                            "login": str,
                            "role": str,
                            "name": str,
                            "surname": str,
                            "patronymic": str,
                            "email": str,
                            "vk_id": int,
                            "telegram_id": int,
                            "is_active": int,
                        },
                        "connect_code": str,
                        "is_active": bool,
                    },
                    "uploaded_at": datetime,
                    "deadline": datetime,
                    "last_updated_at": datetime,
                    "points": [float],
                    "mark_formula": str,
                    "is_active": bool,
                },
                "points": [float],
                "fine": float,
                "mark": float,
                "start_submit": datetime,
                "last_updated_at": datetime,
                "is_active": bool,
            }
        }
    ]
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error


## **Submission**

### Create Submission
- URL: `/api/v0.1/submission/`
- method: **POST**
- auth required: **YES**
- description: 
- request body:
```json
{
    "student_id": str,
    "homework_id": str,
}
```
- response body:
```json
{
    "status": int,
    "submission_id": str,
}
```
- status codes:
  - 200 - OK
  - 400 - Permission denied
  - 500 - Server error

### Get Submission
- URL: `/api/v0.1/submission/{submission_id}`
- method: **GET**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
    "submission": {
        "id": str,
        "student": {
            "id": str,
            "login": str,
            "role": str,
            "name": str,
            "surname": str,
            "patronymic": str,
            "email": str,
            "vk_id": int,
            "telegram_id": int,
            "is_active": bool,
        },
        "homework": {
            "id": str,
            "title": str,
            "file": URL,
            "student_group": {
                "id": str,
                "title": str,
                "teacher": {
                    "id": str,
                    "login": str,
                    "role": str,
                    "name": str,
                    "surname": str,
                    "patronymic": str,
                    "email": str,
                    "vk_id": int,
                    "telegram_id": int,
                    "is_active": int,
                },
                "connect_code": str,
                "is_active": bool,
            },
            "uploaded_at": datetime,
            "deadline": datetime,
            "last_updated_at": datetime,
            "points": [float],
            "mark_formula": str,
            "is_active": bool,
        },
        "points": [float],
        "fine": float,
        "mark": float,
        "start_submit": datetime,
        "last_updated_at": datetime,
        "is_active": bool,
    }
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error

### Edit Submission
- URL: `/api/v0.1/submission/{submission_id}`
- method: **PUT**
- auth required: **YES**
- description: 
- request body:
```json
{
    "points": [float],
    "fine": float,
}
```
- response body:
```json
{
    "status": int,
    "submission_id": str,
}
```
- status codes:
  - 200 - OK
  - 400 - Permission denied
  - 500 - Server error

### Delete Submission
- URL: `/api/v0.1/submission/{submission_id}`
- method: **DELETE**
- auth required: **YES**
- description: 
- response body:
```json
{
    "status": int,
}
```
- status codes:
  - 200 - OK
  - 400 - Auth fail or permission denied
  - 500 - Server error
