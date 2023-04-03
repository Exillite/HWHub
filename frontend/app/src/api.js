import axios from 'axios';

const token = localStorage.getItem('token');

axios.defaults.baseURL = '/api/v0.1';
axios.defaults.headers.common['accept'] = 'application/json';
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.put['Content-Type'] = 'application/json';
if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}


export default {
    async authorize(login, password) {
        return axios.post('/auth/token', { 'username': login, 'password': password }, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            }
        });
    },

    async me() {
        return axios.get('/me');
    },

    async registaration_new_user(login, name, surname, patronymic, email, password) {
        return axios.post('/user', {
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
}