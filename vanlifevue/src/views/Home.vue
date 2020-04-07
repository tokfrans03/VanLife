<template>
  <div class="home">
    <v-card dark class="my-2">
      <v-card-title>Control Panel</v-card-title>
      <v-text-field label="Backend Url" v-model="$store.state.BackendUrl" class="mx-4"></v-text-field>
      <v-card-actions>
        <v-row align="start" justify="space-between">
          <v-col v-if="$store.state.retry" cols="auto">
            <v-btn @click="Get()" color="error">Retry</v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn class="ma-2" color="yellow" @click="refreshconfig()">Refresh Backend</v-btn>
            <v-btn class="ma-2" color="primary" @click="cons()">Console</v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn
              :disabled="Object.entries(config).length === 0"
              @click="connect()"
              color="success"
              class="ma-2"
            >connect</v-btn>
            <v-btn class="ma-2" color="success" :disabled="!check()" @click="sub()">subscribe</v-btn>
          </v-col>
        </v-row>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import { mapGetters } from "vuex";
var mqtt = require("mqtt");

export default {
  name: "home",
  components: {},
  data: () => ({
    config: {},
    connected: false,
    client: undefined,
    load: false,
  }),
  async mounted() {
    this.Get();
  },
  computed: {
    ...mapGetters(["BackendUrl", "retry"])
  },
  methods: {
    Get() {
      axios
        .get(this.$store.state.BackendUrl)
        .then(response => {
          // console.log(response);
          this.$store.state.config = response.data.value.config;
          this.config = response.data.value.config;
          this.$store.state.snac_text = "Loaded config";
          this.$store.state.snac = true;
          this.$store.state.retry = false;
        })
        .catch(error => {
          // console.log(error);
          this.$store.state.snac_text = "Unable to get config";
          this.$store.state.snac = true;
          this.$store.state.retry = true;
        });
    },
    refreshconfig() {
      axios
        .get(this.$store.state.BackendUrl + "refresh")
        .catch(error => {
          this.$store.state.snac_text = "Unable to reach backend";
          this.$store.state.snac = true;
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
    
    connect() {
      var mqtt_url = this.$store.state.config.mqtt.url;
      var url = "mqtt://" + mqtt_url;
      var options = {
        port: this.config.mqtt.port,
        clientId:
          "mqttjs_" +
          Math.random()
            .toString(16)
            .substr(2, 8),
        username: this.$store.state.config.mqtt.user,
        password: this.$store.state.config.mqtt.pass
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
      this.$store.state.config.mqtt.topics.forEach(topic => {
        this.client.subscribe(topic);
      });
      this.$store.state.snac_text = "Subscribed";
      this.$store.state.snac = true;
    },
    cons() {
      console.log(this.load);
      if (this.check()) {
        this.client.publish(this.$store.state.config.mqtt.topics[0], "HHHHHHeeelooooo");
      }
    }
  }
};
</script>
