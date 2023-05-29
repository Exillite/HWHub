<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title @click="$router.push({ name: 'Main' })"
        >ЛОГО</v-toolbar-title
      >
      <v-spacer></v-spacer>
      <router-link to="login" v-if="isSignedOut() && $route.name !== 'Login'">
        <v-btn text>
          Войти
        </v-btn>
      </router-link>
      <router-link to="registration" v-if="isSignedOut() && $route.name !== 'Registration'">
        <v-btn text>
          Зарегистрироваться
        </v-btn>
      </router-link>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import { useLocale } from "vuetify";
import control from "@/control";

export default {
  setup() {
    const { current } = useLocale();

    return {
      changeLocale: (locale) => (current.value = locale),
      isSignedOut: () => !control.check_auth()
    };
  },
};
</script>
