<template>
<div class="hi">
</div>
</template>

<script>

    import api from '@/api'
    import control from '@/control';

    export default {
        data() {
            return {
                hi: 'hi!',
            }
        },
        mounted() {

            if (control.check_auth()){
                this.$router.push({name: 'Shops'});
            } else {
                this.$router.push({name: 'Login'});
            }

            // api.test().then((response) => {
            //     console.log(response);
            //     this.hi = response.data.message;
            // })
        },
    }
</script>

<style>

</style>