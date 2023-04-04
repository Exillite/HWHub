API Documentation
**Документаия к API находится в разработке и будет сильно изменина в ближайшее время**

## __Objects__

- [__Objects__](#objects)
  - [User](#user)
  - [StudentGroup](#studentgroup)
  - [Homework](#homework)
  - [Submission](#submission)

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
```
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
```
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
```
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
```
{
    "id": 987654,
    "student": {
        "id": "654321",
        "login": "johnsmith",
        "role": "student",
        "name": "John",
        "surname": "Smith",
        "patronymic": null,
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