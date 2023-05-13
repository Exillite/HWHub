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
        <v-row align="stretch">
          <v-col
            v-for="(group, index) in groups"
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
                    {{ group.title }}
                  </div>
                  <div class="text-caption">
                    {{ group.teacher.name }} {{ group.teacher.surname }}
                  </div>
                </div>
              </v-card-item>

              <v-card-actions>
                <v-btn
                  @click="
                    $router.push({ name: 'Group', params: { id: group.id } })
                  "
                  variant="outlined"
                >
                  Открыть
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <v-btn
          v-if="user.role === 'teacher' || user.role === 'admin'"
          @click="new_group_dialog = true"
          variant="outlined"
          size="x-large"
          class="new-group-btn"
          color="info"
        >
          Создать новую группу
        </v-btn>

        <v-btn
          v-if="user.role === 'student' || user.role === 'consultant'"
          @click="group_connect_dialog = true"
          variant="outlined"
          size="x-large"
          class="new-group-btn"
          color="info"
        >
          Присоедениться к группе
        </v-btn>
      </v-container>
    </v-main>
  </v-app>

  <v-dialog v-model="new_group_dialog">
    <v-card title="Создание новой группы">
      <form @submit.prevent="submit_create">
        <v-card-text>
          <v-text-field
            v-model="new_group_form.title"
            label="Название группы"
            type="text"
            variant="outlined"
            required
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="outlined"
            @click="new_group_dialog = false"
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

  <v-dialog v-model="group_connect_dialog">
    <v-card title="Присоедениться к группы">
      <form @submit.prevent="submit_connect">
        <v-card-text>
          <v-text-field
            v-model="connect_group_form.code"
            label="Код группы"
            type="text"
            variant="outlined"
            required
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="outlined"
            @click="group_connect_dialog = false"
            color="error"
            >Отмена</v-btn
          >
          <v-btn variant="outlined" type="submit" color="success"
            >Присоедениться</v-btn
          >
        </v-card-actions>
      </form>
    </v-card>
  </v-dialog>
</template>

<script>
import api from "@/api.js";
import control from "@/control";

export default {
  data() {
    return {
      user: {},
      groups: [],
      error: false,
      error_msg: "Ошибка",
      new_group_dialog: false,
      group_connect_dialog: false,
      new_group_form: {
        title: "",
      },
      connect_group_form: {
        code: "",
      },
    };
  },

  mounted() {
    if (!control.check_auth()) {
      this.$router.push({ name: "Login" });
    }

    api.me().then((response) => {
      if (response.data.status == 200) {
        let data = response.data;
        this.user = data.user;

        api.get_all_users_stdents_groups(this.user.id).then((res) => {
          if (res.data.status == 200) {
            this.groups = res.data.student_groups;
          }
        });
      }
    });
  },

  methods: {
    submit_create() {
      api
        .create_new_student_group(this.new_group_form.title, this.user.id)
        .then((response) => {
          if (response.data.status == 200) {
            this.new_group_dialog = false;
            this.new_group_form.title = "";

            api.get_all_users_stdents_groups(this.user.id).then((res) => {
              if (res.data.status == 200) {
                this.groups = res.data.student_groups;
              }
            });
          }
        });
    },

    submit_connect() {
      api
        .connect_me_to_student_group(this.connect_group_form.code)
        .then((response) => {
          if (response.data.status == 200) {
            this.group_connect_dialog = false;
            this.connect_group_form.code = "";

            api.get_all_users_stdents_groups(this.user.id).then((res) => {
              if (res.data.status == 200) {
                this.groups = res.data.student_groups;
              }
            });
          }
        });
    },
  },
};
</script>

<style>
.new-group-btn {
  position: absolute;
  bottom: 0;
  right: 0;

  margin: 40px;
}
</style>
