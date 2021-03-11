<template>
  <div>
    <b-card bg-variant="light" class="bCard">
      <form class="register" @submit.prevent="handlerRegister">
        <h3>Sign Up</h3>
        <div class="RegisterForm">
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
            <label>Token</label>
            <input
              required
              v-model="token"
              class="form-control form-control-lg"
              type="text"
              placeholder="Token"
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
          <div class="form-group">
            <label>Confirm Password</label>
            <input
              required
              v-model="confirmPassword"
              class="form-control form-control-lg"
              type="password"
              placeholder="Confirm Password"
            />
          </div>
          <button type="submit" class="btn btn-dark btn-lg btn-block">
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
  name: "Register",
  data() {
    return {
      username: this.username,
      password: this.password,
      confirmPassword: this.confirmPassword,
      token: this.token,
      message: this.message,
    };
  },
  methods: {
    handlerRegister() {

      if(this.confirmPassword != this.password){
        this.message = "Passwords don't match";
        return
      }
    
      this.message = "";
      this.axios({
        method: "post",
        url: "/register",
        baseURL:
          settings.backend.protocol + settings.URL + settings.backend.path,
        data: {
            username: this.username,
            password: this.password,
            token: this.token,
        },
      })
        .then((response) => {
          sessionStorage.setItem("session_token", response.data.token);
          this.$router.push({ name: "devices" });
        })
        .catch((error) => {
          this.message =
            error.response.status + " - " + error.response.statusText;
        });
    },
  },
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
