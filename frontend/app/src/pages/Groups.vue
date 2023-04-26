<template>
    <v-app>
        <v-app-bar app>
            <v-toolbar-title @click="$router.push({ name: 'Main' })">ЛОГО</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn @click="$router.push({ name: 'Registration' })" text>Зарегистрироваться</v-btn>
        </v-app-bar>
        <v-main>
            <v-container>
                <v-row align="stretch">
                    <v-col v-for="(group, index) in groups" :key="index" cols="12" sm="6" md="4" lg="3">
                        <v-card variant="outlined">
                            <v-card-item>
                                <div>
                                    <div class="text-h6 mb-1">
                                        {{ group.title }}
                                    </div>
                                    <div class="text-caption">{{ group.teacher.name }} {{ group.teacher.surname }}</div>
                                </div>
                            </v-card-item>

                            <v-card-actions>
                                <v-btn variant="outlined">
                                    Открыть
                                </v-btn>
                            </v-card-actions>
                        </v-card>

                    </v-col>

                    <v-col cols="12" sm="6" md="4" lg="3">
                        <v-btn variant="outlined">
                            Создать
                        </v-btn>

                    </v-col>
                </v-row>

            </v-container>

        </v-main>

    </v-app>
</template>

<script>
import api from '@/api.js'

export default {
    data() {
        return {
            groups: [
                {
                    id: "123456",
                    title: "Compu 01",
                    teacher: {
                        id: "789012",
                        login: "janedoe",
                        role: "teacher",
                        name: "Jane",
                        surname: "Doe",
                        patronymic: "R.",
                        email: "janedoe@example.com",
                        vk_id: null,
                        telegram_id: null,
                        is_active: true
                    },
                    connect_code: "abc123",
                    is_active: true,
                },
                {
                    id: "123456",
                    title: 'dsadsa',
                    teacher: {
                        id: "789012",
                        login: "janedoe",
                        role: "teacher",
                        name: "Jane",
                        surname: "Doe",
                        patronymic: "R.",
                        email: "janedoe@example.com",
                        vk_id: null,
                        telegram_id: null,
                        is_active: true
                    },
                    connect_code: "abc123",
                    is_active: true,
                }

            ],
            error: false,
            error_msg: 'Ошибка',
        }
    },
}
</script>

<style></style>
