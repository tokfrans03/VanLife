<template>
  <div>
    <v-toolbar dark>
      <v-toolbar-title>Vanlife</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-toolbar-items>
        <v-btn :loading="$store.state.Get_loading" @click="Get(true);">
          <v-icon dark>mdi-refresh</v-icon>
        </v-btn>
        <v-btn v-for="(link, i) in links" :key="i" :to="link.path">
          {{link.name}}
          <v-badge class="pa-1" v-if="$store.state.updateavailable & link.name == 'Settings'" color="green" dot></v-badge>
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
  </div>
</template>

<script>
import paths from "@/router/paths";
import { mapGetters, mapMutations } from "vuex";

export default {
  data: () => ({}),
  mounted() {
    this.Get(true);
    setInterval(() => {
      this.Get(false, true);
    }, 90 * 1000);
  },
  computed: {
    links() {
      return paths;
    },
    ...mapGetters(["Get_loading"])
  },
  methods: {
    ...mapMutations({
      Get: "Get", // map `this.Get()` to `this.$store.commit('Get')`
      Get_weather: "Get_weather",
      Get_geo: "Get_geo",
      check_update: "check_update"
    })
  }
};
</script>