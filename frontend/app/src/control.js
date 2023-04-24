import cookie from "@/cookie"

export default {

    check_auth() {
        const token = cookie.getCookie('token');
        const user_id = cookie.getCookie('user_id');
        if (token === undefined || user_id === undefined) {
            return false;
        }
        return true;
    },

    log_out() {
        cookie.deleteCookie('token');
        cookie.deleteCookie('user_id');
    },
}