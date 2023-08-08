<script>
import { avatarUrl } from "@/gravatar.js"

export default {
    data() {
        return {
            count: 0
        }
    },
    methods: { avatarUrl },
    props: ['user']
};
</script>

<template>
    <v-avatar :image="avatarUrl(user.email)" class="mr-3"></v-avatar>

    <p class="fon">
        {{ user.name }} {{ user.surname }}
        {{ user.patronymic }}
    </p>
</template>