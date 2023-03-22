<template>
  <v-text-field label="Login" v-model="formData.username"></v-text-field>
  <v-text-field label="PSWD" v-model="formData.password"></v-text-field>
  <v-btn
    @click="auth"
  >Login</v-btn>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {
        formData: {
          username: '',
          password: '',
        },
        token: '',
      }
    },
    methods: {
      auth() {
        axios.post("/api/v0.1/token", this.formData, {
          headers: {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
          }
        }).then((r) => {
          console.log(r);
          this.token = r.data.access_token;
          localStorage.setItem('token', this.token)

          axios.get("/api/v0.1/users/me/", {
            headers: {
              Authorization: `Bearer ${this.token}`,
            }
          }).then((r) => {
              console.log(r);
          })
        });
      },
    },

    mounted() {
      const token = localStorage.getItem('token');
      axios.get("/api/v0.1/users/me/", {
        headers: {
          Authorization: `Bearer ${token}`,
        }
      }).then((r) => {
          console.log(r);
      })
    },
  }
</script>

<style>

</style>