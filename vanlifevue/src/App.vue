<template>
  <v-app dark>
    <toolbar />
    <router-view class="px-8 py-8" />
    <v-snackbar :color="$store.state.snac_color" v-model="$store.state.snac" :timeout="10000">
      {{ $store.state.snac_text }}
      <v-btn text @click="$store.state.snac = false">Close</v-btn>
    </v-snackbar>
  </v-app>
</template>

<script>
import toolbar from "@/components/toolbar.vue";
import { mapGetters } from "vuex";

export default {
  name: "App",

  components: {
    toolbar
  },
  computed: {
    ...mapGetters(["snac", "snac_text", "snac_color"])
  },

  data: () => ({
    //
  })
};
</script>

