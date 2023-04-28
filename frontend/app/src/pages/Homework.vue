<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title @click="$router.push({ name: 'Main' })"
        >ЛОГО</v-toolbar-title
      >
      <v-spacer></v-spacer>
      <v-btn @click="$router.push({ name: 'Registration' })" text
        >Зарегистрироваться</v-btn
      >
    </v-app-bar>
    <v-main>
      <v-container>
        <div class="text-center">
          <h1>{{ homework.title }}</h1>
        </div>
        <p>
          Создано: <b>{{ date_format(homework.uploaded_at) }}</b>
        </p>
        <p>
          Последние изменение:
          <b>{{ date_format(homework.last_updated_at) }}</b>
        </p>
        <p>
          Срок сдачи: date_formate<b>{{ date_format(homework.deadline) }}</b>
        </p>
        <p>
          Формула расчёта оценки: <b>{{ homework.mark_formula }}</b>
        </p>

        <v-tabs v-model="tab" align-tabs="center">
          <v-tab value="tasks">Задания</v-tab>
          <v-tab value="marks">Оценки</v-tab>
          <v-tab value="settings">Настройки</v-tab>
        </v-tabs>
        <br />
        <v-window v-model="tab">
          <v-window-item value="tasks">
            <v-row align="stretch">
              <v-col :key="index" cols="12" sm="6" md="4" lg="3">
                <v-card variant="outlined">
                  <v-card-item>
                    <div>
                      <div class="text-h6 mb-1">
                        {{
                          homework.file.substring(
                            homework.file.lastIndexOf("/") + 1
                          )
                        }}
                      </div>
                    </div>
                  </v-card-item>

                  <v-card-actions>
                    <v-btn variant="outlined"> Скачать </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
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
                  <v-text-field
                    variant="outlined"
                    label="Срок сдачи"
                    type="datetime-local"
                    v-model="new_dedline"
                    required
                  ></v-text-field>
                  <v-table density="compact" hover="true">
                    <thead>
                      <tr>
                        <th class="text-left">Номер задания</th>
                        <th class="text-left">Кол. балов</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="ind in new_points.length">
                        <td>{{ ind }}</td>
                        <td>
                          <v-text-field
                            v-model="new_points[ind - 1]"
                            variant="underlined"
                            type="number"
                          ></v-text-field>
                        </td>
                      </tr>
                    </tbody>
                  </v-table>
                  <v-btn variant="outlined" @click="new_points.push(1)"
                    >Добавить занятие</v-btn
                  >
                  <br />
                  <br />

                  <v-text-field
                    v-model="new_mark_formula"
                    variant="outlined"
                    label="Формула расчётка оценки"
                    required
                  ></v-text-field>

                  <v-btn variant="outlined" type="submit" class="mt-2"
                    >Сохранить</v-btn
                  >
                </v-form>
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
      new_title: "aboba",
      new_dedline: null,
      new_mark_formula: null,
      new_points: [1, 1, 1, 1],

      homework: {
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

      headers: [
        { text: "ФИО", value: "user", fixed: true },
        { text: "1", value: "1" },
        { text: "2", value: "2" },
        { text: "3", value: "3" },
        { text: "Штраф", value: "fine" },
        { text: "Оценка", value: "mark" },
      ],

      items: [
        {
          user: "Alexander Rodionov Vladimirovich",
          1: 1,
          2: 0.2,
          3: 2,
          fine: 1,
          mark: 10,
        },
      ],
      tab: null,
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

<style>
table,
th,
td {
  border: 0.5px groove #666666;
}
</style>
