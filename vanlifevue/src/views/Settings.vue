<template>
  <div class="home">
    <v-card dark class="my-2">
      <v-card-title>Control Panel</v-card-title>
      <v-text-field label="Backend Url" v-model="$store.state.BackendUrl" class="mx-4"></v-text-field>
      <v-card-actions>
        <v-row align="start" justify="space-between">
          <v-col v-if="$store.state.retry" cols="auto">
            <v-btn @click="Get(true)" :loading="$store.state.Get_loading" color="error">Retry</v-btn>
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
    <v-card class="my-2">
      <v-card-title primary-title>Location</v-card-title>
      <v-form class="pa-4">
        <v-text-field label="Lat-long" v-model="$store.state.geo"></v-text-field>
        <v-text-field label="Stad" v-model="$store.state.stad"></v-text-field>
        <v-btn color="success" @click="Get_geo()">Get current</v-btn>
      </v-form>
    </v-card>

    <v-card>
      <v-row>
        <v-col>
          <v-card-title primary-title>Update files</v-card-title>
          <v-btn
            class="ml-4"
            color="success"
            :loading="$store.state.load"
            @click="check_update(); $store.state.load= true"
          >Check for update</v-btn>
          <v-switch class="ml-4" label="Advancerat" v-model="advanced"></v-switch>
        </v-col>
        <v-col cols="auto">
          <span class="mr-4">version {{$store.state.ver}}</span>
        </v-col>
      </v-row>
      <v-card v-if="advanced" class="ma-4 lighten-2">
        <v-card-title primary-title>
          Egen upgradeings url
        </v-card-title>
        <v-form class="pa-4">
          <v-text-field
            label="Url till zip"
            v-model="url"
          ></v-text-field>
          <v-btn color="error" @click="update(url)">UpgraderaEgen upgradeings url</v-btn>
        </v-form>
      </v-card>
      <v-card-actions v-if="$store.state.updateavailable" class="ma-4">
        <v-card>
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">{{$store.state.updateinfo.name}}</h3>
              <div>Säppt {{$store.state.time}}</div>
            </div>
          </v-card-title>
          <div class="ma-4">{{$store.state.updateinfo.body}}</div>
          <v-divider></v-divider>
          <v-card-actions>
            <v-row>
              <v-col cols="auto">
                <v-btn
                  color="error"
                  :loading="load1"
                  @click="update($store.state.updateurl); load1 = true"
                >update to {{$store.state.updateinfo.tag_name}}</v-btn>
              </v-col>
              <v-col>
                <v-alert type="warning" v-model="updating">Sida upgraderas, den kommer tillbaka om ca 1 min</v-alert>
              </v-col>
            </v-row>
          </v-card-actions>
        </v-card>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import moment from "moment";
import { mapGetters, mapMutations } from "vuex";
var mqtt = require("mqtt");

export default {
  name: "Dashboard",
  components: {},
  data: () => ({
    config: {},
    connected: false,
    client: undefined,
    load1: false,
    updating: false,
    advanced: false,
    url: ""
  }),
  computed: {
    ...mapGetters(["BackendUrl", "retry"])
  },
  methods: {
    ...mapMutations({
      Get: "Get", // map `this.add()` to `this.$store.commit('increment')`
      Get_geo: "Get_geo",
      check_update: "check_update"
    }),
    update(url) {
      let data = {
        action: "update",
        value: url
      };
      axios
        .post(this.$store.state.BackendUrl, data)
        .catch(error => {
          this.$store.state.snac_text = error;
          this.$store.state.snac = true;
          this.load1 = false;
        })
        .then(response => {
          // console.log(response)
          this.load1 = false;
          this.updating = true;
          this.$store.state.snac = true;
          this.$store.state.snac_text = response.data.value;
          this.$store.state.snac_color = response.data.Success
            ? "success"
            : "error";
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
      if (this.check()) {
        this.client.publish(
          this.$store.state.config.mqtt.topics[0],
          "HHHHHHeeelooooo"
        );
      }
    }
  }
};
</script>
