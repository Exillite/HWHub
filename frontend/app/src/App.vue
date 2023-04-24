<template>
  <v-app>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
  import { useLocale } from 'vuetify'

  export default {
    setup () {
      const { current } = useLocale()

      return {
        changeLocale: locale => current.value = locale
      }
    }
  }

</script>
