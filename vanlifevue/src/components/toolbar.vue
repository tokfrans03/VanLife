<template>
  <div>
    <v-toolbar dark prominent dense>
      <span class="display-1 mt-7">Vanlife</span>
      <v-spacer></v-spacer>
      <v-toolbar-items id="scroll-target" class="overflow-x-auto">
        <v-btn :loading="$store.state.Get_loading" @click="Get(true);">
          <v-icon dark>mdi-refresh</v-icon>
        </v-btn>
        <v-btn v-for="(link, i) in links" :key="i" :to="link.path">
          {{link.name}}
          <v-badge
            class="pa-1"
            v-if="$store.state.updateavailable & link.name == 'Inställnignar'"
            color="green"
            dot
          ></v-badge>
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
    if (localStorage.getItem("BackendUrl")) {
      this.$store.state.BackendUrl = localStorage.getItem("BackendUrl");
    } else {
      let url = new URL(window.location.href);
      url.port = "8000";
      url.protocol = "https:";
      url.pathname = "";
      this.$store.state.BackendUrl = url.toString();
      localStorage.setItem("BackendURL", this.$store.state.BackendUrl);
      // console.log(this.$store.state.BackendUrl);
    }
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