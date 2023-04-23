<template>
    <body>
        <div class="login-container">
            <Header></Header>
            <input class="input-block" placeholder="Логин..." type="text" style="margin-top: 188px;">
            <input class="input-block" placeholder="Пароль..." type="text" style="margin-top: 32px;">
            <div class="enter-block">
                <div class="enter-block-button" @click="saveLoginFunc"></div>
                <div class="enter-block-text">Сохранить вход</div>
                <div class="enter-block-registration" >Еще не зарегистрированы?</div>
            </div>
            <button class="enter-button">Войти</button>
        </div>
    </body>

</template>

<script>
import Header from '../components/HeaderPage.vue'

export default {
    data () {
        return {
            saveLogin: true
        }
    },
    methods: {
        saveLoginFunc () {
            if (this.saveLogin == true) {
                const saveLoginBtn = document.querySelector('.enter-block-button');
                saveLoginBtn.style.background = "transparent";
                this.saveLogin = false;
            }
            else {
                const saveLoginBtn = document.querySelector('.enter-block-button');
                saveLoginBtn.style.background = 'url("img/save_login_button.3589347a.svg")';
                this.saveLogin = true;

            }
        }
    },
    components: {
        Header
    }
    
}

</script>