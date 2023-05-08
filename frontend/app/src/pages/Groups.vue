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
                <v-btn variant="outlined"> Открыть </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <v-btn
          variant="outlined"
          size="x-large"
          class="new-group-btn"
          color="info"
        >
          Создать новую группу
        </v-btn>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import api from "@/api.js";

export default {
  data() {
    return {
      uesr: null,
      groups: [],
      error: false,
      error_msg: "Ошибка",
    };
  },

  mounted() {
    api.me().then((response) => {
      if (response.data.status == 200) {
        let data = response.data;
        this.uesr = data.user;

        api.get_all_users_stdents_groups(this.uesr.id).then((res) => {
          if (res.data.status == 200) {
            this.groups = res.data.student_groups;
          }
        });
      }
    });
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
