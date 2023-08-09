<template>
    <v-container>
        <div class="text-center">
            <span class="text-grey-darken-3">
                <UserReference :user="group.teacher ?? {}" />
                пригласил(а) вас в
            </span>
            <h1>{{ group.title }}</h1>
            <v-btn variant="outlined" type="submit" color="green" class="mt-5" @click="accept">Принять</v-btn>
        </div>

    </v-container>
</template>

<script>
import api from "@/api.js";
import UserReference from "@/components/UserReference.vue";

async function fetchAll(code) {
    let response = await api.get_invite_data(code);

    if (response.data.status == 200) {
        return response.data.student_group;
    }

    return {};
}

export default {
    data() {
        return {
            group: {},
        };
    },
    async beforeRouteEnter(to, from, next) {
        let data = await fetchAll(to.params.code)
        next(c => c.group = data);
    },
    methods: {
        accept() {
            api
                .connect_me_to_student_group(this.$route.params.code)
                .then((response) => {
                if (response.data.status == 200) {
                    this.$router.push({ name: "Group", params: { id: this.group.id }});
                }
            });
        },
    },
    components: { UserReference }
};
</script>