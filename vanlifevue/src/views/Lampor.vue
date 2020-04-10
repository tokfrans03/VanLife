<template>
  <v-card class="ma-4">
    <v-card-title primary-title>
      <v-icon>lightbulb-on</v-icon>
      <div>
        <!-- <v-icon v-if="config.lamp">mdi-lightbulb-on</v-icon> <v-icon v-else>mdi-lightbulb-off</v-icon> -->
        <h3 class="headline mb-0">Lampor</h3>
        <div>Kontrolera lamporna med dessa knappar</div>
      </div>
    </v-card-title>
    <v-card-actions>
      <v-row align="start" justify="space-between">
        <v-btn
          v-for="(x, i) in this.$store.state.config.codes"
          :key="`${i}-${x}`"
          text
          @click="send_rf(x.code)"
          primary
        >{{x.name}}</v-btn>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  name: "Lampor",
  computed: {
    ...mapGetters(["config"])
  },
  methods: {
    send_rf(code) {
      let data = { action: "rf", value: code };
      axios
        .post(this.$store.state.BackendUrl, data)
        .then(response => {
          // console.log(response);

          this.$store.state.snac_text = response.data.Success
            ? response.data.value
            : "Something went wrong: " + response.data.value;

          this.$store.state.snac_color = response.data.Success
            ? "succes"
            : "error";

          this.$store.state.snac = true;
        })
        .catch(error => {
          this.$store.state.snac_text = "Unable to set light status: " + error;
          this.$store.state.snac_color = "error";
          this.$store.state.snac = true;
        });
    }
  }
};
</script>