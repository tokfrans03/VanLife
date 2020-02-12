<template>
  <div class="home">
    <v-card dark class="my-2">
      <v-card-title>Control Panel</v-card-title>
      <v-text-field label="Backend Url" v-model="Backend_Url" class="mx-4"></v-text-field>
      <v-card-actions>
        <v-btn color="success" @click="Get()">Get data</v-btn>
        <v-btn color="success" @click="refreshconfig()">Refresh Backend</v-btn>
        <v-btn
          :disabled="Object.entries(config).length === 0"
          @click="connect()"
          color="success"
        >connect</v-btn>
        <v-btn color="primary" @click="cons()">Console</v-btn>
      </v-card-actions>
    </v-card>
    <v-card></v-card>
    <v-snackbar v-model="snacc">
      {{snacc_text}}
      <v-btn text color="error" @click.native="snac = false">Close</v-btn>
    </v-snackbar>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
var mqtt = require("mqtt");

export default {
  name: "home",
  components: {},
  created() {},
  data: () => ({
    Backend_Url: "http://192.168.0.67/",
    config: {},
    connected: false,
    snacc: false,
    snacc_text: "Unable to "
  }),
  methods: {
    Get() {
      axios
        .get(this.Backend_Url)
        .then(response => {
          console.log(response);
          this.config = response.data.config;
        })
        .catch(error => {
          this.snacc_text += "get config";
          this.snacc = true;
        });
    },
    refreshconfig() {
      axios.get(this.Backend_Url + "refresh").catch(error => {
        this.snacc_text += "reach backend";
        this.snacc = true;
      });
    },
    connect() {
      var mqtt_url = this.config.mqtt.url;
      var url = "mqtt://" + mqtt_url;
      var options = {
        port: this.config.mqtt.port,
        clientId:
          "mqttjs_" +
          Math.random()
            .toString(16)
            .substr(2, 8),
        username: this.config.mqtt.user,
        password: this.config.mqtt.pass
      };
      console.log("connecting");
      this.client = mqtt.connect(url, options);
      this.client
        .on("error", function(error) {
          console.log("Error");
        })
        .on("close", function(error) {
          console.log("no");
          this.Alert = true;
          this.connected = false;
        });
      this.connected = true;
    },
    cons() {
      console.log(this.config);
    }
  }
};
</script>
