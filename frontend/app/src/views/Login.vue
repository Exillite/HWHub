<template>
            <h2>Вход</h2>
        <form @submit.prevent="submit">
            <v-text-field
                v-model="email"
                label="E-mail"
                type="email"
                variant="outlined"
                required
                autocomplete="email"
            ></v-text-field>
            <v-text-field
                v-model="password"
                label="Пароль"
                variant="outlined"
                type="password"
                required
                autocomplete="current-password"
            ></v-text-field>
            <v-btn variant="outlined" type="submit" color="primary">Войти</v-btn>
        </form>
</template>

<script>
  export default {
    data: () => ({ drawer: null }),
  }
</script>