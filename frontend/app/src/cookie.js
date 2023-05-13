export default {
    getCookie(name) {
        let matches = document.cookie.match(
            new RegExp(
                "(?:^|; )" +
                name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
                "=([^;]*)"
            )
        );
        return matches ? decodeURIComponent(matches[1]) : undefined;
    },

    setCookie(name, value, age) {
        let updatedCookie =
            encodeURIComponent(name) + "=" + encodeURIComponent(value);

        for (let optionKey in age) {
            updatedCookie += "; " + optionKey;
            let optionValue = age[optionKey];
            if (optionValue !== true) {
                updatedCookie += "=" + optionValue;
            }
        }

        document.cookie = updatedCookie;
    },

    deleteCookie(name) {
        this.setCookie(name, "", {
            "max-age": -1,
        });
    },
};