<template>
  <div class="home">
    <v-card dark class="my-2">
      <v-card-title>Control Panel</v-card-title>
      <v-text-field label="Backend Url" v-model="Backend_Url" class="mx-4"></v-text-field>
      <v-card-actions>
        <v-btn color="yellow" @click="refreshconfig()">Refresh Backend</v-btn>
        <v-btn
          :disabled="Object.entries(config).length === 0"
          @click="connect()"
          color="success"
        >connect</v-btn>
        <v-btn color="success" :disabled="!check()" @click="sub()">subscribe</v-btn>
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
    Backend_Url: "http://localhost:8000/",
    config: {},
    connected: false,
    client: undefined,
    snacc: false,
    snacc_text: "Unable to "
  }),
  async mounted() {
    this.Get();
  },
  methods: {
    Get() {
      axios
        .get(this.Backend_Url)
        .then(response => {
          // console.log(response);
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
    check() {
      if (this.client) {
        return this.client.connected;
      } else {
        return false;
      }
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
      let conf = this.config;

      this.client
        .on("connect", function() {
          console.log("connected!!!");
        })
        .on("message", function(topic, message) {
          // message is Buffer
          console.log(message.toString());
        })
        .on("error", function(error) {
          console.log(error);
        })
        .on("close", function(error) {
          console.log(error);
          console.log("closed");
          this.Alert = true;
          this.connected = false;
        });
      this.connected = true;
    },
    sub() {
      this.config.mqtt.topics.forEach(topic => {
        this.client.subscribe(topic);
      });
      this.snacc_text = "Subscribed";
      this.snacc = true;
    },
    cons() {
      if (this.check()) {
        this.client.publish(
          this.config.mqtt.topics[0],
          "HHHHHHeeelooooo"
        );
      }
    }
  }
};
</script>
