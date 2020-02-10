<template>
  <div class="home">
    <v-card dark class="my-2">
      <v-card-title>Control Panel</v-card-title>
      <v-card-actions>
        <v-btn color="success" @click="Get()">Get data</v-btn>
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
    config: {}
  }),
  methods: {
    Get() {
      axios
        .get(this.Backend_Url)
        .then(response => {
          console.log(response)
          this.config = response
        });
    }
  }
};
</script>
