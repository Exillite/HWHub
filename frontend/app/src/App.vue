<template>
<<<<<<< HEAD
  <body>
    <div class="app">
      <router-view></router-view>
    </div>
  </body>
</template>

<script>
export default{
  components:{
  }
}
=======
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

>>>>>>> a6e30e615dd691b7af8ccb08d2f53e38166c268f
</script>
<style>
</style>

