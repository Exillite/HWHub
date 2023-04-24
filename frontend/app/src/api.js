import Axios from 'axios';
import cookie from '@/cookie'

const api_url = '/api/v1';

export default {

    async test() {
        return Axios.post("http://localhost:8000/api", {}, {
            params: {
                token: cookie.getCookie('token'),
            }
        });
    },

    async register(name, surname, login, email, password) {
        return Axios.post(api_url + '/register', {
            name: name,
            surname: surname,
            login: login,
            email: email,
            password: password,
        });
    },

    async login(email, password) {
        return Axios.post(api_url + '/login', {
            email: email,
            password: password
        });
    },

    async create_shop(title) {
        return Axios.post(api_url + "/shop", {
            title: title,
        }, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            }
        })
    },

    async get_shop(shop_slug) {
        return Axios.get(api_url + `/shop/${shop_slug}`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async get_all_users_shops() {
        return Axios.get(api_url + "/user/shops", {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            }
        })
    },

    async add_shop_admin(user_email, shop_slug) {
        return Axios.post(api_url + `/shop/${shop_slug}/admin`, {
            email: user_email,
        }, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            }
        })
    },

    async create_product(title, category, price, coef, slug, shop_id) {
        return Axios.post(api_url + "/product", {
            title: title,
            category: category,
            price: price,
            slug: slug,
            coef: coef,
            shop_id: shop_id,
        }, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            }
        })
    },

    async get_shops_products(shop_slug) {
        return Axios.get(api_url + `/shop/${shop_slug}/products`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async get_product(product_slug) {
        return Axios.get(api_url + `/product/${product_slug}`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        });
    },

    async delete_product(product_slug) {
        return Axios.delete(api_url + `/product/${product_slug}`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        });
    },

    async update_product(product_slug, title, category, price, coef) {
        return Axios.put(api_url + `/product/${product_slug}`, {
            title: title,
            category: category,
            price: price,
            coef: coef,
        }, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async get_item(item_id) {
        return Axios.get(api_url + `/item/${item_id}`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async delete_item(item_id) {
        return Axios.delete(api_url + `/item/${item_id}`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        });
    },

    async create_item(product_id, params) {
        // params example: {cnt: 2, a: 1, b: 2}
        return Axios.post(api_url + "/item", {
            product_id: product_id,
            params: params,
        }, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            }
        })
    },

    async update_item(item_id, params) {
        // params example: {cnt: 2, a: 1, b: 2}
        return Axios.put(api_url + `/item/${item_id}`, {
            params: params,
        }, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            }
        })
    },

    async get_products_items(product_slug) {
        return Axios.get(api_url + `/product/${product_slug}/items`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async create_tempalte(title, shop_id, products) {
        // products example: {"products": [{ "product_id": "string" }, { "product_id": "string" }]}
        return Axios.post(api_url + "/template", {
            title: title,
            shop_id: shop_id,
            products: products,
        }, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            }
        })
    },

    async get_shops_templates(shop_slug) {
        return Axios.get(api_url + `/shop/${shop_slug}/templates`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async get_template(template_id) {
        return Axios.get(api_url + `/template/${template_id}`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async delete_template(template_id) {
        return Axios.delete(api_url + `/template/${template_id}`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async create_order(shop_id, items) {
        // items example: {cnt: 2, items: [{"item_id": "string", cnt: 2, a: "float", b: "float"}, {"item_id": "string", cnt: 1, a: "float"}]}
        return Axios.post(api_url + "/order", {
            shop_id: shop_id,
            items: items,
        }, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            }
        })
    },

    async order_price(shop_id, items) {
        // items example: {cnt: 2, items: [{"item_id": "string", cnt: 2, a: "float", b: "float"}, {"item_id": "string", cnt: 1, a: "float"}]}
        return Axios.post(api_url + "/order/price", {
            shop_id: shop_id,
            items: items,
        }, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            }
        })
    },

    async get_order(order_id) {
        return Axios.get(api_url + `/order/${order_id}`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async delete_order(order_id) {
        return Axios.delete(api_url + `/order/${order_id}`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async get_shops_orders(shop_id) {
        return Axios.get(api_url + `/shop/${shop_id}/orders`, {
            params: {
                token: cookie.getCookie('token'),
                user_id: cookie.getCookie('user_id'),
            },
        })
    },

    async get_tmplate_prices(template_type, data) {
        return Axios.post(api_url + `/price/${template_type}`, {
            data: data,
        });
    },
}