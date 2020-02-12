<template>
  <div class="home">
    <v-card dark class="my-2">
      <v-card-title>Control Panel</v-card-title>
      <v-card-actions>
        <v-btn color="success" @click="Get()">Get data</v-btn>
        <v-btn :disabled="config" @click="connect" color="success">connect</v-btn>
      </v-card-actions>
    </v-card>
    <v-card>
      
    </v-card>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";

export default {
  name: "home",
  components: {},
  created() {},
  data: () => ({
    Backend_Url: "http://192.168.0.67/",
    config: {},
    connected: false
  }),
  methods: {
    Get() {
      axios
        .get(this.Backend_Url)
        .then(response => {
          console.log(response)
          this.config = response
        });
    },
    connect() {
      var mqtt_url = this.config.mqtt.url
      var url = "mqtt://" + mqtt_url;
      var options = {
        port: 8883,
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
  }
};
</script>
