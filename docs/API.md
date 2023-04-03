# API Documentation
# Документаия к API находится в разработке и будет сильно изменина в ближайшее время

## __Objects__

- [User](#user)
- [StudentGroup](#studentgroup)
- [Homework](#homework)
- [Submission](#submission)

---
### User
- id - unique identifier primary key
- role (string) - role of user ("student" | "consultant", "teacher" | "admin" | "user")
- name (string) - first name
- surname (string)  - last name
- patronymic (string) - middle name
- email (string) - email
- vk_id (int) - vk id (optional)
- telegram_id (int) - telegram id (optional)
- students_groups (array of StudentGroup) - student groups
- is_active (bool) - is user active

### StudentGroup
- id - unique identifier primary key
- title (string) - title of group
- teacher (User) - teacher of group
- connect_code (string) - code for connecting to group
- is_active (bool) - is group active

### Homework
- id - unique identifier primary key
- title (string) - title of homework
- file (string) - link to file
- student_group (StudentGroup) - student group
- uploaded_at (datetime) - date and time of upload
- deadline (datetime) - deadline date and time
- last_updated_at (datetime) - date and time of last update
- points (array of double) - points for each task
- mark_formula (string) - formula for calculating mark
- is_active (bool) - is homework active

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


## Methods


### Registration
- method: POST
- path: /api/v0_1/registration
- request body: 
```json
{
    "name": "string",
    "surname": "string",
    "patronymic": "string",
    "email": "string",
    "password": "string",
}
```

- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int"   
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - user with this email already exists
    - 202 - invalid email
    - 203 - invalid password
    - 300 - server error


### Login
- method: POST
- path: /api/v0_1/login
- request body: 
```json
{
    "email": "string",
    "password": "string",
}
```
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int"   
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 202 - invalid email
    - 203 - invalid password
    - 204 - wrong email or password
    - 300 - server error

### Get user
- method: GET
- path: /api/v0_1/user/{id}
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
        "role": "string",
        "name": "string",
        "surname": "string",
        "patronymic": "string",
        "email": "string",
        "vk_id": "int", // if user is not connected to vk, this field is null
        "telegram_id": "int", // if user is not connected to telegram, this field is null
        "students_groups": ["array of StudentGroup`s ids"]
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - user with this id does not exist
    - 300 - server error


### Edit user
- method: PUT
- path: /api/v0_1/user/{id}
- request body: 
```json
{
    "name": "string",
    "surname": "string",
    "patronymic": "string",
}
```
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - user with this id does not exist
    - 300 - server error

### Get from User only consultants
- method: GET
- path: /api/v0_1/user/consultants
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "count": "int",
        "consultants": ["array of User"]
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 200 - no consultants
    - 300 - server error

- example of response body:
```json
{
    "status": 100,
    "data": 
    {   
        "count": 1,
        "consultants": 
        [
            {
                "id": 1,
                "role": "consultant",
                "name": "Ivan",
                "surname": "Ivanov",
                "patronymic": "Ivanovich",
                "email": "test@mai.com",
                "vk_id": 123456789,
                "telegram_id": 123456789,
                "students_groups": [1, 2, 5]
            }
        ]
    }
}
```

### Get Student from StudentGroup
- method: GET
- path: /api/v0_1/student_group/{id}/students
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "count": "int",
        "students": ["array of User"]
    }
}
```

- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 200 - student group has no students
    - 201 - student group with this id does not exist
    - 300 - server error

### Get students groups
- method: GET
- path: /api/v0_1/students_groups
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "count": "int",
        "students_groups": ["array of StudentGroup"]
    }
}
```
- example of response body:
```json
{
    "status": 100,
    "data": 
    {   
        "count": 1,
        "students_groups": 
        [
            {
                "id": 1,
                "title": "Group 1",
                "teacher": 
                {
                    "id": 1,
                    "role": "teacher",
                    "name": "Ivan",
                    "surname": "Ivanov",
                    "patronymic": "Ivanovich",
                    "email": "test@mail.com",
                    "vk_id": null,
                    "telegram_id": 234254253452,
                    "students_groups": [2, 4]
                },
                "connect_code": "123456"
            },
        ]
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 300 - server error

### Get StudentGroup
- method: GET
- path: /api/v0_1/student_group/{id}
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
        "title": "string",
        "teacher": "User",
        "connect_code": "string"
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - student group with this id does not exist
    - 300 - server error

- example of response body:
```json
{
    "status": 100,
    "data": 
    {   
        "id": 1,
        "title": "Group 1",
        "teacher": 
        {
            "id": 1,
            "role": "teacher",
            "name": "Ivan",
            "surname": "Ivanov",
            "patronymic": "Ivanovich",
            "email": "test@mail.ru",
            "vk_id": null,
            "telegram_id": 234254253452,
            "students_groups": [2, 4]
        },
        "connect_code": "123456"
    }
}
```


### Create StudentGroup
- method: POST
- path: /api/v0_1/student_group
- request body: 
```json
{
    "title": "string",
}
```
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 300 - server error

### Edit StudentGroup
- method: PUT
- path: /api/v0_1/student_group/{id}
- request body: 
```json
{
    "title": "string",
}
```
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
        "title": "string",
        "teacher": "User",
        "connect_code": "string"
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - student group with this id does not exist
    - 300 - server error

### Delete StudentGroup
- method: DELETE
- path: /api/v0_1/student_group/{id}
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - student group with this id does not exist
    - 300 - server error

### Get Homework
- method: GET
- path: /api/v0_1/homework/{id}
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
        "title": "string",
        "file": "string",
        "uploaded_at": "datetime",
        "deadline": "datetime",
        "last_updated_at": "datetime",
        "points": ["array of double"],
        "mark_formula": "string"
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - homework with this id does not exist
    - 300 - server error
- example of response body:
```json
{
    "status": 100,
    "data": 
    {
        "id": 1,
        "title": "Homework 1",
        "file": "https://example.com/file.pdf",
        "uploaded_at": "2020-01-01T00:00:00",
        "deadline": "2020-01-01T00:00:00",
        "last_updated_at": "2020-01-01T00:00:00",
        "points": [5.0, 4.0, 3.0],
        "mark_formula": "k - 10",
    }
}
```

### Get Homeworks of StudentGroup
- method: GET
- path: /api/v0_1/student_group/{id}/homeworks
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "count": "int",
        "homeworks": ["array of Homework"]
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - student group with this id does not exist
    - 300 - server error
- example of response body:
```json
{
    "status": 100,
    "data": 
    {   
        "count": 1,
        "homeworks": 
        [
            {
                "id": 1,
                "title": "Homework 1",
                "file": "https://example.com/file.pdf",
                "uploaded_at": "2020-01-01T00:00:00",
                "deadline": "2020-01-01T00:00:00",
                "last_updated_at": "2020-01-01T00:00:00",
                "points": [1.0, 2.0, 3.0],
                "mark_formula": "k / 2 + 1",
            }
        ]
    }
}
```

### Create Homework
- method: POST
- path: /api/v0_1/homework
- request body: 
```json
{
    "title": "string",
    "file": "string",
    "student_group": "int",
    "deadline": "datetime",
    "points": ["array of double"],
    "mark_formula": "string"
}
```
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - student group with this id does not exist
    - 300 - server error

### Edit Homework
- method: PUT
- path: /api/v0_1/homework/{id}
- request body: 
```json
{
    "title": "string",
    "file": "string",
    "deadline": "datetime",
    "points": ["array of double"],
    "mark_formula": "string"
}
```
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
        "title": "string",
        "file": "string",
        "uploaded_at": "datetime",
        "deadline": "datetime",
        "last_updated_at": "datetime",
        "points": ["array of double"],
        "mark_formula": "string"
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - student group with this id does not exist
    - 300 - server error

### Delete Homework
- method: DELETE
- path: /api/v0_1/homework/{id}
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - homework with this id does not exist
    - 300 - server error

### Get Submission of Homework by Student
- method: GET
- path: /api/v0_1/homework/{id}/submission/{student_id}
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
        "points": ["array of double"],
        "points_sum": "double",
        "fine": "double",
        "mark": "double",
        "start_submit": "datetime",
        "last_updated_at": "datetime",
    }
}
```
- example of response body:
```json
{
    "status": 100,
    "data": 
    {
        "id": 1,
        "points": [1.0, 2.0, 3.0],
        "points_sum": 6.0,
        "fine": 0.0,
        "mark": 3.0,
        "start_submit": "2020-01-01T00:00:00",
        "last_updated_at": "2020-01-01T00:00:00",
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - homework with this id does not exist
    - 202 - student with this id does not exist
    - 203 - student does not belong to this student group
    - 300 - server error

### Edit Submission of Homework by Student
- method: PUT
- path: /api/v0_1/homework/{id}/submission/{student_id}
- request body: 
```json
{
    "points": ["array of double"],
    "fine": "double",
}
```
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "id": "int",
        "points": ["array of double"],
        "points_sum": "double",
        "fine": "double",
        "mark": "double",
        "start_submit": "datetime",
        "last_updated_at": "datetime",
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - homework with this id does not exist
    - 202 - student with this id does not exist
    - 203 - student does not belong to this student group
    - 300 - server error

### Get Submissions of Homework
- method: GET
- path: /api/v0_1/homework/{id}/submissions
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "count": "int",
        "submissions": ["array of Submission"]
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - homework with this id does not exist
    - 300 - server error

- example of response body:
```json
{
    "status": 100,
    "data": 
    {   
        "count": 1,
        "submissions": 
        [
            {
                "student_id": 1,
                "student_name": "Ivan",
                "student_surname": "Ivanov",
                "student_patronymic": "Ivanovich",
                "points": [1.0, 0.5, 0.2],
                "points_sum": 12.0,
                "fine": 0.0,
                "mark": 5.0,
                "last_updated_at": "2020-01-01T00:00:00",
            },
        ]
    }
}
```
- note: if student has no homework result, then he will have 0.0 points, 0.0 fine and 0.0 mark


### Get HomeworkResults from StudentGroup
- method: GET
- path: /api/v0_1/student_group/{id}/homework_results
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "count": "int",
        "homework_results": ["array of HomeworkResult"]
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - student group with this id does not exist
    - 300 - server error

- example of response body:
```json
{
    "status": 100,
    "data": 
    {   
        "count": 2,
        "students_count": 2,
        "homework_results": 
        [
            {
                "homework_id": 1,
                "homework_title": "Homework 1",
                "homework_file": "https://example.com/file.pdf",
                "homework_deadline": "2020-01-01T00:00:00",
                "homework_points": [1.0, 2.0, 3.0],
                "homework_mark_formula": "k / 2 + 1",
                "students":
                [
                    {
                        "student_id": 1,
                        "student_name": "Ivan",
                        "student_surname": "Ivanov",
                        "student_patronymic": "Ivanovich",
                        "points": [1.0, 0.5, 0.2],
                        "points_sum": 12.0,
                        "fine": 0.0,
                        "mark": 5.0,
                        "last_updated_at": "2020-01-01T00:00:00",
                    },
                    {
                        "student_id": 2,
                        "student_name": "Petr",
                        "student_surname": "Petrov",
                        "student_patronymic": "Petrovich",
                        "points": [0.0, 0.0, 0.0],
                        "points_sum": 0.0,
                        "fine": 0.0,
                        "mark": 0.0,
                        "last_updated_at": "2020-01-01T00:00:00",
                    }
                ]
            },
            {
                "homework_id": 2,
                "homework_title": "Homework 1",
                "homework_file": "https://example.com/file.pdf",
                "homework_deadline": "2020-01-01T00:00:00",
                "homework_points": [1.0, 2.0, 3.0],
                "homework_mark_formula": "k / 2 + 1",
                "students":
                [
                    {
                        "student_id": 1,
                        "student_name": "Ivan",
                        "student_surname": "Ivanov",
                        "student_patronymic": "Ivanovich",
                        "points": [1.0, 0.5, 0.2],
                        "points_sum": 12.0,
                        "fine": 0.0,
                        "mark": 5.0,
                        "last_updated_at": "2020-01-01T00:00:00",
                    },
                    {
                        "student_id": 2,
                        "student_name": "Petr",
                        "student_surname": "Petrov",
                        "student_patronymic": "Petrovich",
                        "points": [0.0, 0.0, 0.0],
                        "points_sum": 0.0,
                        "fine": 0.0,
                        "mark": 0.0,
                        "last_updated_at": "2020-01-01T00:00:00",
                    }
                ]
            }
        ]
    }
}
```
- note: if student has no homework result, then he will have 0.0 points, 0.0 fine and 0.0 mark


### Get Student HomeworkResults
- method: GET
- path: /api/v0_1/student/{id}/homework_results
- response body: 
```json
{
    "status": "int",
    "data": 
    {
        "count": "int",
        "homework_results": ["array of HomeworkResult"]
    }
}
```
- status codes:
    - 100 - success
    - 103 - success, but server has warnings
    - 201 - student with this id does not exist
    - 300 - server error

- example of response body:
```json
{
    "status": 100,
    "data": 
    {   
        "count": 2,
        "homework_results": 
        [
            {
                "homework_id": 1,
                "homework_title": "Homework 1",
                "homework_file": "https://example.com/file1.pdf",
                "homework_deadline": "2020-01-01T00:00:00",
                "homework_points": [1.0, 2.0, 3.0],
                "homework_mark_formula": "k / 2 + 1",
                "points": [1.0, 0.5, 0.2],
                "points_sum": 12.0,
                "fine": 0.0,
                "mark": 5.0,
                "last_updated_at": "2020-01-01T00:00:00",
            },
            {
                "homework_id": 2,
                "homework_title": "Homework 2",
                "homework_file": "https://example.com/file2.pdf",
                "homework_deadline": "2020-01-01T00:00:00",
                "homework_points": [1.0, 2.0, 3.0],
                "homework_mark_formula": "k / 2 + 1",
                "points": [1.0, 0.5, 0.2],
                "points_sum": 12.0,
                "fine": 0.0,
                "mark": 5.0,
                "last_updated_at": "2020-01-01T00:00:00",
            }
        ]
    }
}
```
