<template>
  <div>
    <b-card bg-variant="light" class="bCard">
      <form class="login" @submit.prevent="handlerLogin">
        <h3>Sign In</h3>
        <div class="SignInForm">
          <div class="form-group">
            <label>Username</label>
            <input
              required
              v-model="username"
              class="form-control form-control-lg"
              type="text"
              placeholder="Username"
            />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input
              required
              v-model="password"
              class="form-control form-control-lg"
              type="password"
              placeholder="Password"
            />
          </div>
          <button type="submit" class="btn btn-dark btn-lg btn-block">
            Login
          </button>
          <button class="btn btn-dark btn-lg btn-block" v-on:click="handlerRegister">
            Register
          </button>
        </div>
        <p>{{ message }}</p>
      </form>
    </b-card>
  </div>
</template>

<script>
import settings from "../../configs.json";
export default {
  name: "Login",
  data() {
    return {
      username: this.username,
      password: this.password,
      message: this.message,
    };
  },
  methods: {
    handlerRegister(){
      this.$router.push({ name: "register" });
    },
    handlerLogin() {
      this.message = "";
      this.axios({
        method: "post",
        url: "/login",
        baseURL:
          settings.backend.protocol + settings.URL + settings.backend.path,
        data: {
          username: this.username,
          password: this.password,
        },
      })
        .then((response) => {
          sessionStorage.setItem("session_token", response.data.token);
          this.$router.push({ name: "devices" });
        })
        .catch((error) => {
          this.message =
            error.status + " - " + error.statusText;
        });
    },
  },
  mounted() {},
  created() {},
  watch: {},
};
</script>

<style>
.bCard {
  width: 400px;
  margin: auto;
}
html,
body {
  margin: 0px;
  padding: 0px;
  background-color: rgb(221, 221, 221);
}
</style>
