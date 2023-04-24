<template>
    <v-app>
        <v-app-bar app>
            <v-toolbar-title @click="$router.push({name: 'Main'})">ЛОГО</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn 
            text
            @click="$router.push({name: 'Login'})"
            >Войти</v-btn>
        </v-app-bar>
      <v-main>
        <v-container>
            <v-alert
                v-if="error"
                type="error"
                dismissible
            >
                <v-alert-title>Ошибка</v-alert-title>
                <v-alert-description>Данные не корректны</v-alert-description>
            </v-alert>
            <h2>Регистрация</h2>
            <v-form @submit.prevent="submit" v-model="isFormValid">
            <v-text-field
                v-model="form.name"
                label="Имя"
                variant="outlined"
                type="text"
                :rules="nameRules"
                autocomplete="given-name"
            ></v-text-field>
            <v-text-field
                v-model="form.surname"
                label="Фамилия"
                variant="outlined"
                type="text"
                required
                :rules="surnameRules"
                autocomplete="family-name"
            ></v-text-field>
            <v-text-field
                v-model="form.login"
                label="Логин"
                variant="outlined"
                type="text"
                required
                :rules="loginRules"
                autocomplete="nickname"
            ></v-text-field>
            <v-text-field
                v-model="form.email"
                variant="outlined"
                label="E-mail"
                type="email"
                required
                :rules="emailRules"
                autocomplete="email"
            ></v-text-field>
            <v-text-field
                variant="outlined"
                v-model="form.password"
                label="Пароль"
                type="password"
                required
                :rules="passwordRules"
                autocomplete="current-password"
            ></v-text-field>
            <v-text-field
                variant="outlined"
                v-model="form.repit_password"
                label="Повторите пароль"
                type="password"
                required
                :rules="repit_passwordRules"
                autocomplete="current-password"
            ></v-text-field>
            <v-btn variant="outlined" type="submit" color="primary" :disabled="!isFormValid" >Зарегистрироваться</v-btn>
        </v-form>
        </v-container>
      </v-main>
      
    </v-app>
  </template>

<script>
    import api from '@/api'

    export default {
        data() {
            return {
                form: {
                    name: '',
                    surname: '',
                    login: '',
                    email: '',
                    password: '',
                    repit_password: '',
                },
                error: false,
                isFormValid: false,

                nameRules: [
                    value => {
                        if (!value) {
                            return 'Введите имя'
                        } else if (value?.length < 3) {
                            return 'Имя должно быть более длинным'
                        } else {
                            return true
                        }
                    }
                ],
                surnameRules: [
                    v => !!v || 'Введите фамилию',
                    v => (v && v.length > 3) || 'Фамилия должна быть более длинной',
                ],
                loginRules: [
                    v => !!v || 'Введите логин',
                    v => (v && v.length > 3) || 'Логин должен быть более длинным',
                ],
                emailRules: [
                    v => !!v || 'Введите E-mail',
                    v => /.+@.+\..+/.test(v) || 'E-mail должен быть валидным',
                ],
                passwordRules: [
                    v => !!v || 'Введите пароль',
                    v => (v && v.length > 6) || 'Пароль должен быть более длинным',
                ],
                repit_passwordRules: [
                    v => !!v || 'Введите пароль',
                    v => (v && v.length > 6) || 'Пароль должен быть более длинным',
                    v => (v && v === this.form.password) || 'Пароли не совпадают',
                ],
            }
        },
        methods: {
            submit() {
                api.register(this.form.name, this.form.surname, this.form.login, this.form.email, this.form.password)
                    .then(response => {
                        if (response.data.status == 200) {
                            this.$router.push({name: 'Main'})
                        } else {
                            this.error = true
                        }
                    })
                    .catch(error => {
                        console.log(error)
                        this.error = true
                    })
            },
        }
    }
</script>

<style>
</style>
