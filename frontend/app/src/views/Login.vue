<template>
</template>

<script>
  import api from '@/api';

  export default {
    data: () => ({  }),
    mounted() {
      api.authorize('exil', '16188sasa').then((r) => {
        const token = r.data.access_token;
        localStorage.setItem('token', token);
        console.log(token);
      }).catch((e) => {console.log(e);});

      api.me().then((r) => {
        console.log(r.data);
      })
    },
  }
</script>