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
}