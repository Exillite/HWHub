<template>
    <h2>Регистрация</h2>
    <v-form @submit.prevent="submit">
        
    </v-form>
</template>

<script>
    export default {
        data(){
            return {
                form: {
                    login: '',
                    name: '',
                    surname: '',
                    patronymic: '',
                    password: '',
                    reppassword: '',
                },
            }
        },
    }
</script>