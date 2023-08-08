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

        <br />
        <v-window>
          <v-window-item>
            <h3>Позиция в очереди: N</h3>
            <br />
            <v-btn block variant="outlined" :color="cnct_btn_color"
              >Покинуть очередь</v-btn
            >

            <br />
            <h3>Принимающие консультанты</h3>

            <v-card
              v-for="student in consultants"
              :key="student.id"
              variant="outlined"
              class="d-flex align-center justify-space-between pa-2 ma-2"
            >
              <UserReference :user="student" />
              <v-spacer></v-spacer>
            </v-card>

            <br />
            <h3>Участники очереди</h3>

            <v-card
              v-for="student in students"
              :key="student.id"
              variant="outlined"
              class="d-flex align-center justify-space-between pa-2 ma-2"
              :color="hieghlight_me(student)"
            >
              <UserReference :user="student" />
              <v-spacer></v-spacer>
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
      user: {
        id: "646b4cc0a9992f8dfa87a4e9",
        login: "exillite",
        role: "admin",
        name: "Alexander",
        surname: "Rodionov",
        patronymic: "Vladimirovich",
        email: "sa27shal@gmail.com",
        vk_id: null,
        telegram_id: null,
        students_groups: [],
        is_active: true,
      },

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

      cnct_btn_color: "error",
      tab: null,

      group: {
        title: "Python",
        teacher: {
          login: "exillite",
          role: "admin",
          name: "Alexander",
          surname: "Rodionov",
          patronymic: "Vladimirovich",
          email: "sa27shal@gmail.com",
          is_active: true,
          id: "646b4cc0a9992f8dfa87a4e9",
          students_groups: [],
        },
        connect_code: "MBTGsd",
        is_active: true,
        id: "646b4d0aa9992f8dfa87a4ea",
      },

      students: [
        {
          id: "646b4cc0a9992f8dfa87a4e9",
          login: "exillite",
          role: "admin",
          name: "Alexander",
          surname: "Rodionov",
          patronymic: "Vladimirovich",
          email: "sa27shal@gmail.com",
          vk_id: null,
          telegram_id: null,
          students_groups: [],
          is_active: true,
        },
      ],

      consultants: [
        {
          id: "646b4cc0a9992f8dfa87a4e9",
          login: "exillite",
          role: "admin",
          name: "Alexander",
          surname: "Rodionov",
          patronymic: "Vladimirovich",
          email: "sa27shal@gmail.com",
          vk_id: null,
          telegram_id: null,
          students_groups: [],
          is_active: true,
        },
      ],
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
  },

  methods: {
    hieghlight_me(student) {
      if (student.id == this.user.id) {
        return "primary";
      }
    },

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

<style></style>
