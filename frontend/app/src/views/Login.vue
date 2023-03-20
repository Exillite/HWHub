<template>
  <v-text-field label="Login" v-model="login"></v-text-field>
  <v-text-field label="PSWD" v-model="pswd"></v-text-field>
  <v-btn
    @click="auth"
  >Login</v-btn>
</template>

<script>
  export default {
    data() {
      return {
        login: '',
        pswd: '',
      }
    },
    methods: {
      auth() {
        
      },
    },
  }
</script>

<style>

</style>