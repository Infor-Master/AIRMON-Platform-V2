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
        <b-navbar-nav class="ml-auto">
          <b-nav-form @submit.prevent="handlerOffset">
            <b-form-input
              size="sm"
              class="mr-sm-2"
              placeholder="Limit"
              v-model="limit"
            ></b-form-input>
            <b-form-input
              size="sm"
              class="mr-sm-2"
              placeholder="Offset"
              v-model="offset"
            ></b-form-input>
            <b-form-select
              v-model="selectedData"
              :options="options"
              size="sm"
              class="mr-sm-2"
            ></b-form-select>
            <b-button type="submit" size="sm" class="my-2 my-sm-0"
              >Search</b-button
            >
          </b-nav-form>
        </b-navbar-nav>
      </b-navbar>
    </div>
    <div>
      <fusioncharts
        type="line"
        width="100%"
        height="400"
        dataFormat="json"
        :dataSource="datasource"
      >
      </fusioncharts>
    </div>
    <div>
      <link
        href="https://fonts.googleapis.com/icon?family=Material+Icons"
        rel="stylesheet"
      />
      <datatable
        title="Leituras Sensores"
        id="sensor-chart"
        :columns="columns"
        :rows="data"
        :clickable="false"
        :printable="false"
        :perPage="[10, 20, 50, 100]"
        :defaultPerPage="20"
      >
      </datatable>
    </div>
  </div>
</template>

<script>
import settings from "../../configs.json";
import VueJwtDecode from "vue-jwt-decode";
import DataTable from "vue-materialize-datatable";

export default {
  components: {
    datatable: DataTable,
  },
  data() {
    return {
      limit: 100,
      offset: 0,
      device: {},
      selectedData: { id:"CO2_PPM", text: "CO2", label: "ppm"},
      options: [
        { value: { id:"CO2_PPM", text: "CO2", label: "ppm"}, text: "CO2 (ppm)" },
        { value: { id:"NO2_PPM", text: "NO2", label: "ppm"}, text: "NO2 (ppm)" },
        { value: { id:"CH2O_PPM", text: "CH2O", label: "ppm"}, text: "CH2O (ppm)" },
        { value: { id:"O3_PPM", text: "O3", label: "ppm"}, text: "O3 (ppm)" },
        { value: { id:"Temp_C", text: "Temperatura", label: "ºC"}, text: "Temperatura (ºC)" },
        { value: { id:"Hum_100", text: "Humidade", label: "%"}, text: "Humidade (%)" },
      ],
      data: [],
      datasource: {},
      columns: [
        {
          label: "Time",
          field: "CreatedAt",
          numeric: false,
          html: false,
        },
        {
          label: "O3 (ppm)",
          field: "O3_PPM",
          numeric: true,
          html: false,
        },
        {
          label: "CO2 (ppm)",
          field: "CO2_PPM",
          numeric: true,
          html: false,
        },
        {
          label: "NO2 (ppm)",
          field: "NO2_PPM",
          numeric: true,
          html: false,
        },
        {
          label: "CH2O (ppm)",
          field: "CH2O_PPM",
          numeric: true,
          html: false,
        },
        {
          label: "Temperatura (ºC)",
          field: "Temp_C",
          numeric: true,
          html: false,
        },
        {
          label: "Humidade (%)",
          field: "Hum_100",
          numeric: true,
          html: false,
        },
      ],
    };
  },
  methods: {
    getDevice() {
      try {
        this.jwtDecoded = VueJwtDecode.decode(
          sessionStorage.getItem("session_token")
        );
        this.axios({
          method: "get",
          url: `/device/` + this.$route.params.id,
          baseURL:
            settings.backend.protocol + settings.URL + settings.backend.path,
          data: {},
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
          },
        })
          .then((response) => {
            this.devices = response.data.data;
            this.getData();
          })
          .catch((error) => {
            this.message = error.status + " - " + error.statusText;
          });
      } catch (error) {
        this.message = error.status + " - " + error.statusText;
      }
    },
    getData() {
      try {
        this.jwtDecoded = VueJwtDecode.decode(
          sessionStorage.getItem("session_token")
        );
        this.axios({
          method: "get",
          url:
            `/data/` +
            this.$route.params.id +
            `/` +
            this.limit +
            `/` +
            this.offset,
          baseURL:
            settings.backend.protocol + settings.URL + settings.backend.path,
          data: {},
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
          },
        })
          .then((response) => {
            console.log(response);
            this.data = [];
            for (var i in response.data.data) {
              this.data.push(response.data.data[i]);
            }
            this.getGraphData(this.selectedData);
          })
          .catch((error) => {
            console.log(error);
            this.message = error.status + " - " + error.statusText;
          });
      } catch (error) {
        console.log(error);
        this.message = error.status + " - " + error.statusText;
      }
    },
    getGraphData(field) {
      this.datasource = {
        chart: {
          caption: "Leituras Sensor " + field.text,
          subCaption: "",
          yAxisName: field.label,
          theme: "fusion",
        },
        data: [],
      };
      for (var i in this.data) {
        this.datasource.data.push({
          label: this.data[i]["CreatedAt"],
          value: this.data[i][field.id],
        });
      }
    },
    handlerOffset() {
      this.getData();
    },
  },
  mounted() {
    this.getDevice();
  },
  created() {},
  watch: {
    selectedData: function (newselectedData) {
      this.getGraphData(newselectedData);
    },
  },
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
