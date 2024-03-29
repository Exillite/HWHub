import axios from "axios";
import control from "@/control";

const token = control.get_authorization_token();

axios.defaults.baseURL = "/api/v0.1";
axios.defaults.headers.common["accept"] = "application/json";
axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers.put["Content-Type"] = "application/json";
if (token) {
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export default {
    async reauthorize() {
        const token = control.get_authorization_token();
        if (token) {
            axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        }
    },

    async authorize(login, password) {
        return axios.post(
            "/auth/token", { username: login, password: password }, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            }
        );
    },

    async me() {
        this.reauthorize();
        return axios.get("/me");
    },

    async register_new_user(
        login,
        name,
        surname,
        patronymic,
        email,
        password
    ) {
        return axios.post("/user", {
            login: login,
            name: name,
            surname: surname,
            patronymic: patronymic,
            email: email,
            password: password,
        });
    },

    async get_user(user_id) {
        return axios.get(`/user/${user_id}`);
    },

    async edit_user(user_id, name, surname, patronymic) {
        return axios.put(`/user/${user_id}`, {
            name: name,
            surname: surname,
            patronymic: patronymic,
        });
    },

    async delete_user(user_id) {
        return axios.delete(`/user/${user_id}`);
    },

    async create_new_student_group(title, teacher_id) {
        return axios.post("/student_group", {
            title: title,
            teacher_id: teacher_id,
        });
    },

    async get_student_group(student_group_id) {
        return axios.get(`/student_group/${student_group_id}`);
    },

    async edit_student_group(student_group_id, title) {
        return axios.put(`/student_group/${student_group_id}`, {
            title: title,
        });
    },

    async delete_student_group(student_group_id) {
        return axios.delete(`/student_group/${student_group_id}`);
    },

    async create_new_homework(
        title,
        files,
        student_group_id,
        deadline,
        points,
        mark_formula
    ) {
        return axios.post("/homework", {
            title: title,
            files,
            student_group_id: student_group_id,
            deadline: deadline,
            points: points,
            mark_formula: mark_formula,
        });
    },

    async get_homework(homework_id) {
        return axios.get(`/homework/${homework_id}`);
    },

    async edit_homework(
        homework_id,
        title,
        files,
        deadline,
        points,
        mark_formula
    ) {
        return axios.put(`/homework/${homework_id}`, {
            title: title,
            files,
            deadline: deadline,
            points: points,
            mark_formula: mark_formula,
        });
    },

    async delete_homework(homework_id) {
        return axios.delete(`/homework/${homework_id}`);
    },

    async create_new_submission(student_id, homework_id) {
        return axios.post("/submission", {
            student_id: student_id,
            homework_id: homework_id,
        });
    },

    async get_submission(submission_id) {
        return axios.get(`/submission/${submission_id}`);
    },

    async edit_submission(submission_id, points, fine) {
        return axios.put(`/submission/${submission_id}`, {
            points: points,
            fine: fine,
        });
    },

    async delete_submission(submission_id) {
        return axios.delete(`/submission/${submission_id}`);
    },

    async get_all_users_students_groups(user_id) {
        return axios.get(`/user/${user_id}/student_groups`);
    },

    async get_all_homeworks_from_student_group(student_group_id) {
        return axios.get(`/student_group/${student_group_id}/homeworks`);
    },

    async get_student_groups_students(student_group_id) {
        return axios.get(`/student_group/${student_group_id}/students`);
    },

    async get_student_groups_consultants(student_group_id) {
        return axios.get(`/student_group/${student_group_id}/consultants`);
    },

    async kick_user_from_students_group(student_group_id, user_id) {
        return axios.patch(
            `/student_group/${student_group_id}/kick_user/${user_id}`
        );
    },

    async add_user_to_students_group(student_group_id, user_id) {
        return axios.patch(
            `/student_group/${student_group_id}/add_user/${user_id}`
        );
    },

    async get_student_group_results(student_group_id) {
        return axios.get(`/student_group/${student_group_id}/get_results`);
    },

    async get_homework_results(homework_id) {
        return axios.get(`/homework/${homework_id}/submissions`);
    },

    async upload_files(files) {
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append("files", files[i]);
        }

        return axios.post("/files/upload", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
    },

    async get_student_group_marks(student_group_id) {
        return axios.get(`/student_group/${student_group_id}/get_marks`);
    },

    async get_homework_marks(homework_id) {
        return axios.get(`/homework/${homework_id}/marks`);
    },

    async get_invite_data(student_group_code) {
        return axios.get(`/user/connect/${student_group_code}`);
    },

    async connect_me_to_student_group(student_group_code) {
        return axios.patch(`/user/connect/${student_group_code}`);
    },
};