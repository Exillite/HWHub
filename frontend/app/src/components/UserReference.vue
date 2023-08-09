<script>
import { avatarUrl } from "@/gravatar.js"

export default {
    computed: {
        avatarUrl() {
            return this.user?.email ? avatarUrl(this.user.email) : "";
        }
    },
    props: {
        user: {
            type: Object,
            required: true
        },
        noPatronymic: {
            type: Boolean,
            default: false
        } 
    }
};
</script>

<template>
    <span class="fon">
        <v-avatar :image="avatarUrl" class="mr-1" />
    
        {{ user.name }}
        {{ user.surname }}
        <template v-if="!noPatronymic">
        {{ user.patronymic }}
        </template>
    </span>
</template>