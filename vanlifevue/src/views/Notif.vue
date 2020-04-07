<template>
  <div>
    <v-card width="500" class="ma-4">
      <v-card-title primary-title>Lägg till personer</v-card-title>
      <v-form class="px-4" v-model="add_form">
        <v-text-field label="Namn" :rules="required_rule" v-model="name"></v-text-field>
        <v-text-field label="User" :rules="required_rule" v-model="user"></v-text-field>
        <v-text-field label="Key" :rules="required_rule" v-model="key"></v-text-field>
      </v-form>
      <v-card-actions>
        <v-btn color="success" :loading="loading1" :disabled="!add_form" @click="add">lägg till</v-btn>
        <v-select class="px-2" :items="personer" label="Personer" v-model="person" ></v-select>
        <v-btn color="error" :loading="loading2" :disabled="!Boolean(person)" @click="remove()">ta bort</v-btn>
        <!-- <v-btn color="error">ta bort</v-btn> -->
      </v-card-actions>
    </v-card>

    <v-card width="500" class="ma-4">
      <v-form v-model="send" class="pa-4">
        <v-text-field name="url" label="url" v-model="$store.state.BackendUrl"></v-text-field>
        <v-text-field name="title" label="Titel" v-model="title" :rules="required_rule"></v-text-field>
        <v-text-field name="message" label="Medelande" v-model="message" :rules="required_rule"></v-text-field>
        <v-text-field name="img" label="Bild URL" v-model="img"></v-text-field>
        <v-btn color="success" :loading="loading" :disabled="!send" @click="send_notif()">send</v-btn>
      </v-form>
      <v-alert :color="response_color" :value="Boolean(response)">{{response}}</v-alert>
    </v-card>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  name: "Notif",
  data() {
    return {
      send: false,
      add_form: false,
      response: "",
      response_color: "error",
      loading: false,
      loading1: false,
      loading2: false,
      title: "",
      message: "",
      img: "",
      user: "",
      key: "",
      name: "",
      required_rule: [v => !!v || "Required"],
      personer: [],
      person: ""
    };
  },
  computed: {
    ...mapGetters(["BackendUrl", "config"])
  },
  mounted() {
    this.$store.state.config.notif.forEach(person => {
      this.personer.push(person.name);
    });
  },
  methods: {
    add() {
      let data = {
        action: "addnotif",
        value: {
          user: this.user,
          key: this.key,
          name: this.name
        }
      };
      let self = this;
      this.loading1 = true;
      let url = this.$store.state.BackendUrl;
      axios
        .post(url, data)
        .then(function(response) {
          self.$store.state.snac = true;
          self.$store.state.snac_text = response.data.value;
          self.$store.state.snac_color = response.data.Success
            ? "success"
            : "error";
          self.loading1 = false;
        })
        .catch(function(error) {
          // handle error
          self.$store.state.snac = true;
          self.$store.state.snac_text = error + "  ==  Is the server running?";
          self.$store.state.snac_color = "error";
          self.loading1 = false;
        });
    },
    remove(){
      let data = {
        action: "removenotif",
        value: {
          name: this.person
        }
      };
      let self = this;
      this.loading2 = true;
      let url = this.$store.state.BackendUrl;
      axios
        .post(url, data)
        .then(function(response) {
          self.$store.state.snac = true;
          self.$store.state.snac_text = response.data.value;
          self.$store.state.snac_color = response.data.Success
            ? "success"
            : "error";
          self.loading2 = false;
        })
        .catch(function(error) {
          // handle error
          self.$store.state.snac = true;
          self.$store.state.snac_text = error + "  ==  Is the server running?";
          self.$store.state.snac_color = "error";
          self.loading2 = false;
        });
    },
    send_notif() {
      let data = {
        action: "notif",
        value: {
          title: this.title,
          message: this.message,
          imgurl: this.img
        }
      };
      let self = this;
      this.loading = true;
      let url = this.$store.state.BackendUrl;
      axios
        .post(url, data)
        .then(function(response) {
          self.$store.state.snac = true;
          self.$store.state.snac_text = response.data.value;
          self.$store.state.snac_color = response.data.Success
            ? "success"
            : "error";
          self.loading = false;
        })
        .catch(function(error) {
          // handle error
          self.$store.state.snac = true;
          self.$store.state.snac_text = error + "  ==  Is the server running?";
          self.$store.state.snac_color = "error";
          self.loading = false;
        });
    }
  }
};
</script>