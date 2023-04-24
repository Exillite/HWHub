<template>
    <v-app>
        <v-app-bar app>
            <v-toolbar-title
            @click="$router.push({name: 'Main'})">ЛОГО</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn 
            @click="$router.push({name: 'Registration'})"
            text>Зарегистрироваться</v-btn>
        </v-app-bar>
      <v-main>
        <v-container>
            <v-alert
                v-if="error"
                type="error"
                title="Ошибка"
                variant="outlined"
                dismissible
            > {{ error_msg }}
            </v-alert>
            <h2>Вход</h2>
            <form @submit.prevent="submit">
            <v-text-field
                v-model="form.login"
                label="Логин"
                type="text"
                variant="outlined"
                required
                autocomplete="nickname"
            ></v-text-field>
            <v-text-field
                v-model="form.password"
                label="Пароль"
                variant="outlined"
                type="password"
                required
                autocomplete="current-password"
            ></v-text-field>
            <v-btn variant="outlined" type="submit" color="primary">Войти</v-btn>
        </form>
        </v-container>

      </v-main>
      
    </v-app>
  </template>

<script>
    import api from '@/api.js'

    export default {
        data() {
            return {
                form: {
                    login: '',
                    password: '',
                },
                error: false,
                error_msg: 'Ошибка',
            }
        },
        methods: {
            submit() {
                api.authorize(this.form.login, this.form.password).then((response) => {
                    console.log(response);
                    if (response.status == 200) {
                        let token = response.data.access_token;
                        localStorage.setItem('token', token)
                        this.$router.push({name: 'Main'});
                    } else {
                        this.error_msg = 'Не верный логин или пароль.'
                        this.error = true;
                    } 
                }).catch((error) => {
                    this.error_msg = 'Не верный логин или пароль.'
                    this.error = true;
                    console.log(error);
                })
            }
        }
    }
</script>

<style>
</style>
