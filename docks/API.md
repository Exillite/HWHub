# API Documentation

## Objects

### User
- id (int) - unique identifier primary key
- name (string) - first name
- surname (string)  - last name
- patronymic (string) - middle name
- email (string) - email
- vk_id (int) - vk id (optional)
- telegram_id (int) - telegram id (optional)
- students_groups (array of StudentGroup) - student groups

### StudentGroup
- id (int) - unique identifier primary key
- title (string) - title of group
- teacher (User) - teacher of group

### Homework
- id (int) - unique identifier primary key
- title (string) - title of homework
- file (string) - link to file
- student_group (StudentGroup) - student group
- uploaded_at (datetime) - date and time of upload
- deadline (datetime) - deadline date and time
- last_updated_at (datetime) - date and time of last update
- points (array of double) - points for each task
- mark_formula (string) - formula for calculating mark

### Submission
- id (int) - unique identifier primary key
- student (User) - student
- homework (Homework) - homework
- points (array of double) - length of array must be equal to length of points array in homework, each element is 1 if task is done, 0 otherwise or percentage of task completion (for example, 0.5 if task is done half)
- fine (double) - fine for late submission (0 if submitted on time)
- mark (double) - mark for submission, calculated by formula in homework
- startsubmit (datetime) - date and time of start of submission
- last_updated_at (datetime) - date and time of last update

