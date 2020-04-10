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
            <v-btn class="ma-2" color="primary" @click="cons()">Sluta ladda</v-btn>
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

    <v-card class="my-4">
      <v-card-title primary-title>Send command</v-card-title>
      <v-form class="pa-4">
        <v-text-field label="Command" v-model="command"></v-text-field>

        <v-btn color="success" :loading="command_load" @click="send_command(command)">send</v-btn>
      </v-form>
      <v-card>
        <div class="ma-8">{{command_out}}</div>
      </v-card>
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
        <v-card-title primary-title>Andra releaser</v-card-title>
        <v-btn color="success" :loading="Get_all_load" @click="Get_all()">Hämta</v-btn>
        <v-select class="px-2" :items="versions" label="Verisoner" v-model="ver"></v-select>

        <v-btn
          v-if="Boolean(ver)"
          color="error"
          :loading="load1"
          @click="update(cross(ver))"
        >Upgradera till {{ver}}</v-btn>

        <v-card-title primary-title>Egen upgradeings url</v-card-title>
        <v-form class="pa-4">
          <v-text-field label="Url till zip" v-model="url"></v-text-field>
          <v-btn
            color="error"
            v-if="Boolean(url)"
            :loading="load1"
            @click="update(url)"
          >Upgradera med Egen url</v-btn>
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
                  @click="update($store.state.updateurl)"
                >update to {{$store.state.updateinfo.tag_name}}</v-btn>
              </v-col>
            </v-row>
          </v-card-actions>
        </v-card>
      </v-card-actions>
      <v-alert type="warning" v-model="updating">Sida upgraderas, den kommer tillbaka snart</v-alert>
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
    Get_all_load: false,
    releases: [],
    versions: [],
    ver: "",
    updating: false,
    advanced: false,
    url: "",
    command: "",
    command_load: false,
    command_out: ""
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
    send_command(command) {
      this.command_load = true;
      let data = {
        action: "command",
        value: command
      };
      axios
        .post(this.$store.state.BackendUrl, data)
        .catch(error => {
          this.$store.snac_text = error;
          this.$store.snac = true;
          this.command_load = false;
        })
        .then(response => {
          this.command_out = response.data.value;
          this.command_load = false;
        });
    },
    cross(ver) {
      for (let index = 0; index < this.releases.length; index++) {
        if (this.releases[index].ver == this.ver) {
          return this.releases[index].url;
        }
      }
    },
    Get_all() {
      let url = "https://api.github.com/repos/tokfrans03/VanLife/releases";
      this.Get_all_load = true;
      axios
        .get(url)
        .catch(error => {
          this.$store.snac_text = error;
          this.$store.snac = true;
          this.Get_all_load = false;
        })
        .then(response => {
          response.data.forEach(element => {
            this.releases.push({
              url: element.assets[0].browser_download_url,
              ver: element.tag_name
            });
            this.versions.push(element.tag_name);
          });
          this.Get_all_load = false;
        });
    },
    update(url) {
      console.log("Upgraderar till:", url);
      let data = {
        action: "update",
        value: url
      };
      this.updating = true;
      this.load1 = true;
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
          this.$store.state.snac = true;
          this.$store.state.snac_text = response.data.value;
          this.$store.state.snac_color = response.data.Success
            ? "success"
            : "error";
          setTimeout(() => {
            location.reload();
          }, 2000);
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
      // if (this.check()) {
      //   this.client.publish(
      //     this.$store.state.config.mqtt.topics[0],
      //     "HHHHHHeeelooooo"
      //   );
      // }
      this.$store.state.load = false;
      this.$store.state.Get_loading = false;
    }
  }
};
</script>
