import cookie from "@/cookie";

export default {
    save_authorization(token) {
        const save_time = 60 * 60 * 24 * 7 * 2; // save on two week

        cookie.setCookie("token", token, save_time);
    },

    get_authorization_token() {
        let token = cookie.getCookie("token");
        if (token === undefined) {
            return false;
        }
        return token;
    },

    check_auth() {
        const token = cookie.getCookie("token");
        if (token === undefined) {
            return false;
        }
        return true;
    },

    log_out() {
        cookie.deleteCookie("token");
    },
};