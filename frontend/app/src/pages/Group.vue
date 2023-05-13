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
          <v-tab
            v-if="
              user.role == 'admin' ||
              user.role == 'consultant' ||
              user.role == 'teacher'
            "
            value="students"
            >Ученики</v-tab
          >
          <v-tab value="marks">Оценки</v-tab>
          <v-tab
            v-if="user.role == 'admin' || user.role == 'teacher'"
            value="settings"
            >Настройки</v-tab
          >
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
                    <v-btn
                      variant="outlined"
                      @click="
                        $router.push({
                          name: 'Homework',
                          params: { id: homework.id },
                        })
                      "
                      >Открыть</v-btn
                    >
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>

            <v-btn
              v-if="user.role === 'teacher' || user.role === 'admin'"
              @click="new_homework_dialog = true"
              variant="outlined"
              size="x-large"
              class="new-homework-btn"
              color="info"
            >
              Добавить задание
            </v-btn>
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
              <v-btn @click="kick_user(student.id)" color="red"
                >Исключить</v-btn
              >
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
                <v-form @submit.prevent="submit_edit_group" variant="outlined">
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
                  v-for="consultant in consultants"
                  :key="consultant.id"
                  variant="outlined"
                  class="d-flex align-center justify-space-between pa-2 ma-2"
                >
                  <p class="fon">
                    {{ consultant.name }} {{ consultant.surname }}
                    {{ consultant.patronymic }}
                  </p>
                  <v-spacer></v-spacer>
                  <v-btn @click="kick_user(consultant.id)" color="red"
                    >Исключить</v-btn
                  >
                </v-card>
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </v-container>
    </v-main>
  </v-app>

  <v-dialog v-model="new_homework_dialog">
    <v-card title="Создание нового задания">
      <form @submit.prevent="submit_create_homework">
        <v-card-text>
          <v-text-field
            v-model="new_homework_form.title"
            label="Название задания"
            type="text"
            variant="outlined"
            required
          ></v-text-field>

          <v-file-input
            v-model="new_homework_form.files"
            multiple
            variant="outlined"
            label="Файлы с заданием"
            prepend-icon=""
          ></v-file-input>

          <v-text-field
            variant="outlined"
            label="Срок сдачи"
            type="datetime-local"
            v-model="new_homework_form.deadline"
            required
          ></v-text-field>

          <v-text-field
            v-model="new_homework_form.mark_formula"
            label="Формула для расчёта оценки"
            type="text"
            variant="outlined"
            required
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="outlined"
            @click="new_homework_dialog = false"
            color="error"
            >Отмена</v-btn
          >
          <v-btn variant="outlined" type="submit" color="success"
            >Создать</v-btn
          >
        </v-card-actions>
      </form>
    </v-card>
  </v-dialog>
</template>

<script>
import api from "@/api.js";
import control from "@/control.js";

export default {
  data() {
    return {
      user: {},

      new_title: "",

      headers: [{ text: "ФИО", value: "user", fixed: true }],

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
        },
      ],

      tab: null,
      group: {},
      homeworks: [],

      students: [],

      consultants: [],

      new_homework_dialog: false,

      new_homework_form: {
        title: "",
        files: [],
        deadline: null,
        points: [1],
        mark_formula: "",
      },
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

    api.get_student_group(this.$route.params.id).then((response) => {
      if (response.data.status == 200) {
        this.group = response.data.student_group;
        this.new_title = this.group.title;

        api.get_all_homeworks_from_student_group(this.group.id).then((res) => {
          if (res.data.status == 200) {
            this.homeworks = res.data.homeworks;
          }
        });

        api.get_student_groups_students(this.group.id).then((res) => {
          if (res.data.status == 200) {
            this.students = res.data.users;
          }
        });

        api.get_student_groups_consultants(this.group.id).then((res) => {
          if (res.data.status == 200) {
            this.consultants = res.data.users;
          }
        });

        api.get_student_group_marks(this.group.id).then((res) => {
          if (res.data.status == 200) {
            this.show_marks();
            this.items = res.data.marks;
          }
        });
      } else {
        this.$router.push({ name: "Error" });
      }
    });
  },

  methods: {
    show_marks() {
      for (let i = 0; i < this.homeworks.length; i++) {
        const homework = this.homeworks[i];
        this.headers.push({
          text: this.date_format(homework.deadline, false),
          value: homework.id,
        });
      }
    },

    submit_create_homework() {
      api.upload_files(this.new_homework_form.files).then((response) => {
        if (response.data.status == 200) {
          api
            .create_new_homework(
              this.new_homework_form.title,
              response.data.files,
              this.group.id,
              this.new_homework_form.deadline,
              this.new_homework_form.points,
              this.new_homework_form.mark_formula
            )
            .then((res) => {
              if (res.data.status == 200) {
                api
                  .get_all_homeworks_from_student_group(this.group.id)
                  .then((r) => {
                    if (r.data.status == 200) {
                      this.homeworks = r.data.homeworks;
                      this.new_homework_dialog = false;

                      this.new_homework_form = {
                        title: "",
                        files: [],
                        deadline: null,
                        points: [1],
                        mark_formula: "",
                      };
                    }
                  });
              }
            });
        }
      });
    },

    submit_edit_group() {
      api.edit_student_group(this.group.id, this.new_title).then((response) => {
        if (response.data.status == 200) {
          api.get_student_group(this.$route.params.id).then((response) => {
            if (response.data.status == 200) {
              this.group = response.data.student_group;
              this.new_title = this.group.title;
            }
          });
        }
      });
    },

    kick_user(user_id) {
      api
        .kick_user_from_students_group(this.group.id, user_id)
        .then((response) => {
          if (response.data.status == 200) {
            api.get_student_groups_students(this.group.id).then((res) => {
              if (res.data.status == 200) {
                this.students = res.data.users;
              }
            });

            api.get_student_groups_consultants(this.group.id).then((res) => {
              if (res.data.status == 200) {
                this.consultants = res.data.users;
              }
            });
          }
        });
    },

    date_format(date_str, with_time = true) {
      let date = new Date(date_str);
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, "0");
      const day = date.getDate().toString().padStart(2, "0");
      const hours = date.getHours().toString().padStart(2, "0");
      const minutes = date.getMinutes().toString().padStart(2, "0");
      if (with_time) return `${day}.${month}.${year} ${hours}:${minutes}`;
      else return `${day}.${month}.${year}`;
    },
  },
};
</script>

<style>
.new-homework-btn {
  position: fixed;
  bottom: 0;
  right: 0;

  margin: 40px;
}
</style>
