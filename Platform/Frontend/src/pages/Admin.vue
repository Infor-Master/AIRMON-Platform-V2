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
        <form class="device" @submit.prevent="handlerAddDevice">
          <h3>Add Device</h3>
          <div class="DeviceForm">
            <div class="form-group">
              <label>Device Name</label>
              <input
                required
                v-model="devname"
                class="form-control form-control-lg"
                type="text"
                placeholder="Device Name"
              />
            </div>
            <div class="form-group">
              <label>Device Key</label>
              <input
                required
                v-model="devtoken"
                class="form-control form-control-lg"
                type="text"
                placeholder="Device Key"
              />
            </div>
            <button type="submit" class="btn btn-dark btn-lg btn-block">
              Create Device
            </button>
          </div>
          <p>{{ addmessage }}</p>
        </form>
      </b-card>
      <b-card bg-variant="light" class="bCard">
        <form class="device" @submit.prevent="handlerRemoveDevice">
          <h3>Remove Device</h3>
          <div class="DeviceForm">
            <div class="form-group">
              <b-form-select
                v-model="devRemove"
                :options="devoptions"
                size="sm"
                class="mr-sm-2"
              />
            </div>
            <button type="submit" class="btn btn-dark btn-lg btn-block">
              Remove Device
            </button>
          </div>
          <p>{{ remmessage }}</p>
        </form>
      </b-card>

      <b-card bg-variant="light" class="bCard">
        <form class="device" @submit.prevent="handlerAddInvite">
          <h3>Add Invite</h3>
          <div class="InviteForm">
            <div class="form-group">
              <label>User email</label>
              <input
                required
                v-model="invname"
                class="form-control form-control-lg"
                type="text"
                placeholder="User email"
              />
            </div>
            <button type="submit" class="btn btn-dark btn-lg btn-block">
              Invite User
            </button>
          </div>
          <p>{{ addmessage }}</p>
        </form>
      </b-card>

       <b-card bg-variant="light" class="bCard">
        <form class="device" @submit.prevent="handlerRemoveInvite">
          <h3>Remove Invite</h3>
          <div class="DeviceForm">
            <div class="form-group">
              <b-form-select
                v-model="devRemoveInvites"
                :options="devInvites"
                size="sm"
                class="mr-sm-2"
              />
            </div>
            <button type="submit" class="btn btn-dark btn-lg btn-block">
              Remove Invite
            </button>
          </div>
          <p>{{ remmessage }}</p>
        </form>
      </b-card>

       <b-card bg-variant="light" class="bCard">
        <form class="device" @submit.prevent="handlerRemoveUser">
          <h3>Remove User</h3>
          <div class="DeviceForm">
            <div class="form-group">
              <b-form-select
                v-model="devRemoveUser"
                :options="devUsers"
                size="sm"
                class="mr-sm-2"
              />
            </div>
            <button type="submit" class="btn btn-dark btn-lg btn-block">
              Remove User
            </button>
          </div>
          <p>{{ remmessage }}</p>
        </form>
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
      addmessage: "",
      remmessage: "",
      devname: this.devname,
      devtoken: this.devtoken,
      devRemove: null,
      devRemoveInvites: null,
      devoptions: [],
      devInvites: [],
      devUsers: [],
      devRemoveUser: null,
      invname: this.invname
    };
  },
  methods: {
     handlerRemoveUser() {

      this.message = "";
      this.axios({
        method: "delete",
        url: "/user",
        baseURL:
          settings.backend.protocol + settings.URL + settings.backend.path,
        data: this.devRemoveUser.user,
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
        },
      })
        .then((response) => {
          this.remmessage = response.data.message;
          this.getUsers()
        })
        .catch((error) => {
          this.remmessage = error.status + " - " + error.statusText;
        });
    },
    getUsers() {
      try {
        this.jwtDecoded = VueJwtDecode.decode(
          sessionStorage.getItem("session_token")
        );
        this.axios({
          method: "get",
          url: "/user",
          baseURL:
            settings.backend.protocol + settings.URL + settings.backend.path,
          data: {},
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
          },
        })
          .then((response) => {
            this.devUsers = [];
            for (var i in response.data.data) {
              this.devUsers.push({
                value: {
                  user: response.data.data[i],
                },
                text: response.data.data[i].Username,
              });
            }
          })
          .catch((error) => {
            this.remmessage =
              error.status + " - " + error.statusText;
          });
      } catch (error) {
        this.remmessage = error.status + " - " + error.statusText;
      }
    },
    handlerAddInvite(){
      this.message = "";
      this.axios({
        method: "post",
        url: "/invite",
        baseURL:
          settings.backend.protocol + settings.URL + settings.backend.path,
        data: {
          username: this.invname
          },
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
        },
      })
        .then((response) => {
          this.addmessage = response.data.message;
        })
        .catch((error) => {
          this.addmessage = error.status + " - " + error.statusText;
        });
    },
    handlerRemoveInvite() {
      console.log(this.devRemoveInvites.invite);

      this.message = "";
      this.axios({
        method: "delete",
        url: "/invite",
        baseURL:
          settings.backend.protocol + settings.URL + settings.backend.path,
        data: this.devRemoveInvites.invite,
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
        },
      })
        .then((response) => {
          this.remmessage = response.data.message;
          this.getInvites()
        })
        .catch((error) => {
          this.remmessage = error.status + " - " + error.statusText;
        });
    },
     getInvites() {
      try {
        this.jwtDecoded = VueJwtDecode.decode(
          sessionStorage.getItem("session_token")
        );
        this.axios({
          method: "get",
          url: "/invite",
          baseURL:
            settings.backend.protocol + settings.URL + settings.backend.path,
          data: {},
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
          },
        })
          .then((response) => {
            this.devInvites = [];
            for (var i in response.data.data) {
              this.devInvites.push({
                value: {
                  invite: response.data.data[i],
                },
                text: response.data.data[i].Username + " - " + response.data.data[i].Token,
              });
            }
          })
          .catch((error) => {
            this.remmessage =
              error.status + " - " + error.statusText;
          });
      } catch (error) {
        this.remmessage = error.status + " - " + error.statusText;
      }
    },
    handlerAddDevice() {
      this.message = "";
      this.axios({
        method: "post",
        url: "/device",
        baseURL:
          settings.backend.protocol + settings.URL + settings.backend.path,
        data: {
          key: this.devtoken,
          name: this.devname,
        },
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
        },
      })
        .then((response) => {
          this.addmessage = response.data.message;
          this.getDevices()
        })
        .catch((error) => {
          this.addmessage = error.status + " - " + error.statusText;
        });
    },
    handlerRemoveDevice() {
      this.message = "";
      this.axios({
        method: "delete",
        url: "/device",
        baseURL:
          settings.backend.protocol + settings.URL + settings.backend.path,
        data: this.devRemove.device,
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
        },
      })
        .then((response) => {
          this.remmessage = response.data.message;
          this.getDevices()
        })
        .catch((error) => {
          this.remmessage = error.status + " - " + error.statusText;
        });
    },
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
            this.devoptions = [];
            for (var i in response.data.data) {
              this.devoptions.push({
                value: {
                  id: response.data.data[i].ID,
                  device: response.data.data[i],
                },
                text: response.data.data[i].Name,
              });
            }
          })
          .catch((error) => {
            this.remmessage =
              error.status + " - " + error.statusText;
          });
      } catch (error) {
        this.remmessage = error.status + " - " + error.statusText;
      }
    },
  },
  mounted() {
    this.getDevices();
    this.getInvites();
    this.getUsers();
  },
  created() {},
  watch: {
  },
};
</script>

<style>
.bCard {
  width: 400px;
  margin: auto;  
}</style>
