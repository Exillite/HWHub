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
                <div class="enter-block-button">
                    <img class="enter-block-button" src="../media/save_login_button.svg">
                </div>
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
    }
}

</script>