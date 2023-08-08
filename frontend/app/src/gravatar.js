import md5 from "md5";

export function hash(email) {
    return md5(email.toLowerCase());
};

export function avatarUrl(email) {
    return "https://www.gravatar.com/avatar/" + hash(email) + "?d=identicon";
};