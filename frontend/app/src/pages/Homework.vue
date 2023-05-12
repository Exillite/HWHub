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
          Срок сдачи: <b>{{ date_format(homework.deadline) }}</b>
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
              <v-col
                v-for="(file, index) in homework.files"
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
                        {{ file.replace("_", " ") }}
                      </div>
                    </div>
                  </v-card-item>

                  <v-card-actions>
                    <v-btn variant="outlined" @click="download_file(file)">
                      Скачать
                    </v-btn>
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
                <v-form
                  @submit.prevent="submit_edit_homework"
                  variant="outlined"
                >
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
                    format="yyyy-MM-ddTHH:mm"
                    v-model="new_dedline"
                    required
                  ></v-text-field>
                  <v-table density="compact" hover="true">
                    <thead>
                      <tr>
                        <th class="text-left">Номер задания</th>
                        <th class="text-left">Кол. балов</th>
                        <th style="width: 10px"></th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="ind in new_points.length">
                        <td>{{ ind }}</td>
                        <td>
                          <v-text-field
                            required
                            v-model="new_points[ind - 1]"
                            variant="underlined"
                            type="number"
                          ></v-text-field>
                        </td>
                        <td>
                          <v-col cols="auto">
                            <v-btn density="compact" icon="mdi-delete"></v-btn>
                          </v-col>
                        </td>
                      </tr>
                    </tbody>
                  </v-table>
                  <v-btn block variant="outlined" @click="new_points.push(1)"
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
import control from "@/control.js";

export default {
  data() {
    return {
      user: {},

      new_title: "",
      new_dedline: null,
      new_mark_formula: null,
      new_points: [],

      homework: {},

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

  mounted() {
    if (!control.check_auth()) {
      this.$router.push({ name: "Login" });
    }

    api.me().then((response) => {
      if (response.data.status == 200) {
        this.user = response.data.user;
      }
    });

    api.get_homework(this.$route.params.id).then((response) => {
      if (response.data.status == 200) {
        this.homework = response.data.homework;

        this.new_title = this.homework.title;
        this.new_dedline = this.homework.deadline;
        this.new_mark_formula = this.homework.mark_formula;
        this.new_points = this.homework.points;
      } else {
        this.$router.push({ name: "Error" });
      }
    });
  },

  methods: {
    download_file(file) {
      const link = document.createElement("a");
      link.href = `/api/v0.1/files/download/${file}`;
      link.download = file;
      link.click();
    },

    submit_edit_homework() {
      api
        .edit_homework(
          this.homework.id,
          this.new_title,
          this.homework.files,
          this.new_dedline,
          this.new_points,
          this.new_mark_formula
        )
        .then((response) => {
          if (response.data.status == 200) {
            api.get_homework(this.homework.id).then((res) => {
              this.homework = res.data.homework;

              this.new_title = this.homework.title;
              this.new_dedline = this.homework.deadline;
              this.new_mark_formula = this.homework.mark_formula;
              this.new_points = this.homework.points;
            });
          }
        });
    },

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

table {
  border-radius: 5px;
}
</style>
