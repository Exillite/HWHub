<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title @click="$router.push({ name: 'Main' })"
        >ЛОГО</v-toolbar-title
      >
      <v-spacer></v-spacer>

    </v-app-bar>
    <v-main>
      <v-container>
        <div class="text-center">
          <h1>{{ group.title }}</h1>
        </div>

        <v-tabs v-model="tab" align-tabs="center">
          <v-tab value="tasks">Задания</v-tab>
          <v-tab value="students">Ученики</v-tab>
          <v-tab value="marks">Оценки</v-tab>
          <v-tab value="settings">Настройки</v-tab>
        </v-tabs>
        <br />
        <v-window v-model="tab">
          <v-window-item value="tasks">
            <v-row align="stretch">
              <v-col
                v-for="(homework, index) in homeworks"
                :key="index"
                cols="12"
                sm="6"
                md="4"
                lg="3"
              >
                <v-card variant="outlined">
                  <v-card-item>
                    <div>
                      <div class="text-h6 mb-1">
                        {{ homework.title }}
                      </div>
                      <div class="text-caption">
                        До
                        {{ date_format(homework.deadline) }}
                      </div>
                    </div>
                  </v-card-item>

                  <v-card-actions>
                    <v-btn variant="outlined"> Открыть </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-window-item>

          <v-window-item value="students">
            <v-card
              v-for="student in students"
              :key="student.id"
              variant="outlined"
              class="d-flex align-center justify-space-between pa-2 ma-2"
            >
              <p class="fon">
                {{ student.name }} {{ student.surname }}
                {{ student.patronymic }}
              </p>
              <v-spacer></v-spacer>
              <v-btn color="red">Исключить</v-btn>
            </v-card>
          </v-window-item>

          <v-window-item value="marks">
            <EasyDataTable
              border-cell
              :headers="headers"
              :items="items"
              hide-footer
            />
          </v-window-item>

          <v-window-item value="settings">
            <v-card variant="outlined" class="ma-2">
              <v-card-item>
                <v-card-title>Параметры</v-card-title>
              </v-card-item>

              <v-card-text>
                <v-form @submit.prevent variant="outlined">
                  <v-text-field
                    v-model="new_title"
                    variant="outlined"
                    label="Название"
                    required
                  ></v-text-field>
                  <v-btn variant="outlined" type="submit" class="mt-2"
                    >Сохранить</v-btn
                  >
                </v-form>
              </v-card-text>
            </v-card>

            <v-card variant="outlined" class="ma-2">
              <v-card-item>
                <v-card-title>Консультанты</v-card-title>
              </v-card-item>

              <v-card-text>
                <v-card
                  v-for="student in students"
                  :key="student.id"
                  variant="outlined"
                  class="d-flex align-center justify-space-between pa-2 ma-2"
                >
                  <p class="fon">
                    {{ student.name }} {{ student.surname }}
                    {{ student.patronymic }}
                  </p>
                  <v-spacer></v-spacer>
                  <v-btn color="red">Исключить</v-btn>
                </v-card>

                <v-btn variant="outlined" type="submit" class="mt-2"
                  >Добавить</v-btn
                >
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import api from "@/api.js";

export default {
  data() {
    return {
      new_title: "sdada",

      headers: [
        { text: "ФИО", value: "user", fixed: true },
        { text: "02.04.23", value: "123" },
        { text: "02.04.23", value: "123" },
        { text: "02.04.23", value: "123" },
        { text: "02.04.23", value: "123" },
        { text: "02.04.23", value: "123" },
        { text: "02.04.23", value: "123" },
        { text: "02.04.23", value: "123" },
        { text: "02.04.23", value: "123" },
        { text: "02.04.23", value: "123" },
      ],

      items: [
        {
          user: "Alexander Rodionov Vladimirovich",
          123: 6,
        },
        {
          user: "Alexander Rodionov Vladimirovich",
          123: 6,
        },
        {
          user: "Alexander Rodionov Vladimirovich",
          123: 6,
        },
      ],

      tab: null,
      group: {
        id: "123456",
        title: "Computer classes 01",
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
          is_active: true,
        },
        connect_code: "abc123",
        is_active: true,
      },
      homeworks: [
        {
          id: "123456",
          title: "Programming Assignment 1",
          file: "https://example.com/programming-assignment-1.pdf",
          student_group: {
            id: "654321",
            title: "Computer Science 101",
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
              is_active: true,
            },
            connect_code: "abc123",
            is_active: true,
          },
          uploaded_at: "2023-04-02T10:00:00Z",
          deadline: "2023-04-09T10:00:00Z",
          last_updated_at: "2023-04-03T15:30:00Z",
          points: [7.5, 5.0, 2.5],
          mark_formula: "(K + 3) / 10",
          is_active: true,
        },
      ],

      students: [
        {
          id: "123456",
          login: "johndoe",
          role: "student",
          name: "Johdskjn",
          surname: "Ddsfahoe",
          patronymic: "Wladimirovich",
          email: "johndoe@example.com",
          vk_id: 123456789,
          telegram_id: 987654321,
          is_active: true,
        },
        {
          id: "123456",
          login: "johndoe",
          role: "student",
          name: "John",
          surname: "Doe",
          patronymic: "Wladimirovich",
          email: "johndoe@example.com",
          vk_id: 123456789,
          telegram_id: 987654321,
          is_active: true,
        },
        {
          id: "123456",
          login: "johndoe",
          role: "student",
          name: "John",
          surname: "Doe",
          patronymic: "Wladimirovich",
          email: "johndoe@example.com",
          vk_id: 123456789,
          telegram_id: 987654321,
          is_active: true,
        },
        {
          id: "123456",
          login: "johndoe",
          role: "student",
          name: "John",
          surname: "Doe",
          patronymic: "Wladimirovich",
          email: "johndoe@example.com",
          vk_id: 123456789,
          telegram_id: 987654321,
          is_active: true,
        },
        {
          id: "123456",
          login: "johndoe",
          role: "student",
          name: "John",
          surname: "Doe",
          patronymic: "Wladimirovich",
          email: "johndoe@example.com",
          vk_id: 123456789,
          telegram_id: 987654321,
          is_active: true,
        },
        {
          id: "123456",
          login: "johndoe",
          role: "student",
          name: "John",
          surname: "Doe",
          patronymic: "Wladimirovich",
          email: "johndoe@example.com",
          vk_id: 123456789,
          telegram_id: 987654321,
          is_active: true,
        },
      ],
    };
  },

  methods: {
    date_format(date_str) {
      let date = new Date(date_str);
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, "0");
      const day = date.getDate().toString().padStart(2, "0");
      const hours = date.getHours().toString().padStart(2, "0");
      const minutes = date.getMinutes().toString().padStart(2, "0");

      return `${day}.${month}.${year} ${hours}:${minutes}`;
    },
  },
};
</script>

<style></style>
