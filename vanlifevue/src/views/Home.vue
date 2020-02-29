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
      <v-alert class="ma-4" type="success" :value="this.Alert">{{Alerttext}}</v-alert>
    </v-card>
    <v-card>
      <v-card-title primary-title>
        <div>
          <h3 class="headline mb-0">Lampor</h3>
          <div>Kontrolera lamporna med dessa knappar</div>
        </div>
      </v-card-title>
      <v-card-actions>
        <v-btn text @click="send(4353281)" primary>on/off</v-btn>
        <v-btn text @click="send(4353287)" primary>100%</v-btn>
       <v-btn text @click="send(4353288)" primary>50%</v-btn>  <!-- Needs better solution -->
        <v-btn text @click="send(4353289)" primary>25%</v-btn>
      </v-card-actions>
    </v-card>
    <v-snackbar v-model="snacc">
      {{snacc_text}}
      <v-btn text color="error" @click="snacc = false" :timeout="2000">Close</v-btn>
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
    Backend_Url: "http://192.168.0.97/",
    config: {},
    connected: false,
    client: undefined,
    load: false,
    snacc: false,
    snacc_text: "",
    Alert: false,
    Alerttext: ""
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
          this.config = response.data.value.config;
          this.snacc_text = "Loaded config";
          this.snacc = true;
        })
        .catch(error => {
          this.snacc_text = "Unable to get config";
          this.snacc = true;
        });
    },
    refreshconfig() {
      axios
        .get(this.Backend_Url + "refresh")
        .catch(error => {
          this.snacc_text = "Unable to reach backend";
          this.snacc = true;
        })
        .then(response => {
          this.Get();
        });
    },
    check() {
      if (this.client) {
        return this.client.connected;
      } else {
        return false;
      }
    },
    send(code) {
      let data = { action: "rf", value: code };
      axios
        .post(this.Backend_Url, data)
        .then(response => {
          // console.log(response);

          if (response.data.Success) {
            this.snacc_text = "Success";
          } else {
            this.snacc_text = "Something went wrong: " + response.data.value;
          }
          this.snacc = true;
        })
        .catch(error => {
          this.snacc_text = "Unable to set light status: " + error;
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
          this.connected = false;
        });
      this.connected = true;
    },
    sub() {
      this.config.mqtt.topics.forEach(topic => {
        this.client.subscribe(topic);
      });
      this.Alerttext = "Subscribed!";
      this.Alert = true;
      this.snacc_text = "Subscribed";
      this.snacc = true;
    },
    cons() {
      console.log(this.load);
      if (this.check()) {
        this.client.publish(this.config.mqtt.topics[0], "HHHHHHeeelooooo");
      }
    }
  }
};
</script>
