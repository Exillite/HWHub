<template>
  <v-app>
    <v-main>
      <v-container>
        <v-alert
          v-if="error"
          type="error"
          title="Ошибка"
          variant="outlined"
          dismissible
        >
          {{ error_msg }}
        </v-alert>
        <h2>Регистрация</h2>
        <v-form @submit.prevent="submit" v-model="isFormValid">
          <v-text-field
            v-model="form.name"
            label="Имя"
            variant="outlined"
            type="text"
            :rules="nameRules"
            autocomplete="given-name"
          ></v-text-field>
          <v-text-field
            v-model="form.surname"
            label="Фамилия"
            variant="outlined"
            type="text"
            required
            :rules="surnameRules"
            autocomplete="family-name"
          ></v-text-field>
          <v-text-field
            v-model="form.patronymic"
            label="Отчество"
            variant="outlined"
            type="text"
            required
            :rules="patronymicRules"
          ></v-text-field>
          <v-text-field
            v-model="form.login"
            label="Логин"
            variant="outlined"
            type="text"
            required
            :rules="loginRules"
            autocomplete="login"
          ></v-text-field>
          <v-text-field
            v-model="form.email"
            variant="outlined"
            label="E-mail"
            type="email"
            required
            :rules="emailRules"
            autocomplete="email"
          ></v-text-field>
          <v-text-field
            variant="outlined"
            v-model="form.password"
            label="Пароль"
            type="password"
            required
            :rules="passwordRules"
            autocomplete="current-password"
          >
            <template v-slot:loader>
              <v-progress-linear
                :color="passwordScoreColor"
                :model-value="passwordScore"
                max="4"
              ></v-progress-linear>
            </template>
          </v-text-field>
          <v-text-field
            variant="outlined"
            v-model="form.repit_password"
            label="Повторите пароль"
            type="password"
            required
            :rules="repeat_passwordRules"
            autocomplete="current-password"
          ></v-text-field>
          <v-btn
            variant="outlined"
            type="submit"
            color="primary"
            :disabled="!isFormValid"
            >Зарегистрироваться</v-btn
          >
        </v-form>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import api from "@/api.js";
import zxcvbn from "zxcvbn";

export default {
  data() {
    return {
      form: {
        login: "",
        name: "",
        surname: "",
        patronymic: "",
        email: "",
        password: "",
        repit_password: "",
      },
      error: false,
      error_msg: "Ошибка!",

      isFormValid: false,

      nameRules: [
        (value) => {
          if (!value) {
            return "Введите имя";
          } else if (value?.length < 3) {
            return "Имя должно быть более длинным";
          } else {
            return true;
          }
        },
      ],
      surnameRules: [
        (v) => !!v || "Введите фамилию",
        (v) => (v && v.length > 3) || "Фамилия должна быть более длинной",
      ],
      patronymicRules: [(v) => !!v || "Введите отчество"],
      loginRules: [
        (v) => !!v || "Введите логин",
        (v) => (v && v.length > 3) || "Логин должен быть более длинным",
      ],
      emailRules: [
        (v) => !!v || "Введите E-mail",
        (v) => /.+@.+\..+/.test(v) || "E-mail должен быть валидным",
      ],
      passwordRules: [
        (v) => !!v || "Введите пароль",
        (v) => (v && v.length > 6) || "Пароль должен быть более длинным",
        (v) => (this.passwordScore > 1) || "Пароль слишком слабый",
      ],
      repeat_passwordRules: [
        (v) => !!v || "Введите пароль",
        (v) => (v && v.length > 6) || "Пароль должен быть более длинным",
        (v) => (v && v === this.form.password) || "Пароли не совпадают",
      ],
    };
  },
  computed: {
    passwordScore() {
      let result = zxcvbn(this.form.password, [this.form.name, this.form.patronymic, this.form.surname, this.form.login]);
      // TODO: possibly show time to crack
      return result.score;
    },
    passwordScoreColor() {
      switch (this.passwordScore) {
        case 0:
          return "red-darken-4";
        case 1:
          return "orange-darken-3";
        case 2:
          return "yellow-darken-1";
        case 3:
          return "lime";
        case 4:
          return "green";
        default:
          return "gray";
      }
    }
  },
  methods: {
    submit() {
      api
        .registaration_new_user(
          this.form.login,
          this.form.name,
          this.form.surname,
          this.form.patronymic,
          this.form.email,
          this.form.password
        )
        .then((response) => {
          switch (response.data.status) {
            case 200:
              this.$router.push({ name: "Main" });
              break;
            case 202:
              this.error_msg =
                "Пользователь с таким E-mail уже зарегестрирован.";
              break;
            case 203:
              this.error_msg = "Не корректный пароль.";
              break;
            case 204:
              this.error_msg =
                "Пользователь с таким Login уже зарегестрирован.";
              break;
            case 500:
            case 400:
              this.error_msg = "Ошибка на сервере";
              break;
          }

          this.error = true;
        })
        .catch((error) => {
          console.log(error);
          this.error = true;
        });
    },
  },
};
</script>

<style></style>
