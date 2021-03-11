<template>
  <div>
    <div>
      <b-navbar toggleable="lg" type="dark" variant="dark" fixed="top">
        <b-navbar-brand href="/#/devices">AIRMON</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse is-nav id="nav-collapse">
            <b-navbar-nav>
                <b-nav-item href="/#/devices">Dispositivos</b-nav-item>
                <b-nav-item href="/#/admin">Admin</b-nav-item>
                <b-nav-item href="/#/logout">Logout</b-nav-item>
            </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <div>
      <b-card bg-variant="light" class="bCard">
        <b-list-group>
          <b-list-group-item
            v-for="(device, index) in devices"
            :key="index"
            @click="deviceHandler(device.ID)"
          >
            {{ device.Name }} - {{ device.Key }}
          </b-list-group-item>
        </b-list-group>
      </b-card>
    </div>
  </div>
</template>

<script>
import settings from "../../configs.json";
import VueJwtDecode from "vue-jwt-decode";
export default {
  data() {
    return {
      devices: [],
    };
  },
  methods: {
    getDevices() {
      try {
        this.jwtDecoded = VueJwtDecode.decode(
          sessionStorage.getItem("session_token")
        );
        this.axios({
          method: "get",
          url: `/device`,
          baseURL:
            settings.backend.protocol + settings.URL + settings.backend.path,
          data: {},
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
          },
        })
          .then((response) => {
            this.devices = [];
            for (var i in response.data.data) {
              this.devices.push(response.data.data[i]);
            }
          })
          .catch((error) => {
            this.message =
              error.response.status + " - " + error.response.statusText;
          });
      } catch (error) {
        this.message =
          error.status + " - " + error.statusText;
      }
    },
    deviceHandler(id) {
      this.$router.push("/devices/" + id);
    },
  },
  mounted() {
    this.getDevices();
  },
  created() {},
  watch: {},
};
</script>

<style>
.bCard {
  width: auto;
  margin: auto;
  padding: 20px;
}
html,
body {
  margin: 0px;
  padding: 0px;
  background-color: rgb(221, 221, 221);
}
</style>
