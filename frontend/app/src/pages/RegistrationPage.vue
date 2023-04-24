<template>
    <body>
        <div class="registration-container">
            <Header></Header>
            <input class="input-block" placeholder="Логин..." type="text" style="margin-top: 188px;">
            <input class="input-block" placeholder="Имя..." type="text" style="margin-top: 16px;">
            <input class="input-block" placeholder="Фамилия..." type="text" style="margin-top: 16px;">
            <input class="input-block" placeholder="Отчество..." type="text" style="margin-top: 16px;">
            <input class="input-block" placeholder="Пароль..." type="text" style="margin-top: 16px;">
            <input class="input-block" placeholder="Повторите пароль..." type="text" style="margin-top: 16px;">
            <div class="enter-block">
                <div class="enter-block-button" @click="acceptAgreements"></div>
                <div class="enter-block-text">Принимаю пользовательское соглашение</div>
            </div>
            <div class="enter-button">Регистрация</div>
        </div>
        
    </body>

</template>

<script>
import Header from '../components/HeaderPage.vue'
export default{
    components: {
        Header
    },
    methods:{
        acceptAgreements () {
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
    }
}

</script>