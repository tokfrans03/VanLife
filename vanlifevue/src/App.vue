<template>
  <v-app dark>
    <toolbar />
    <router-view class="px-8 py-8" />
  </v-app>
</template>

<script>
import toolbar from "@/components/toolbar.vue";

export default {
  name: "App",

  components: {
    toolbar
  },

  data: () => ({
    //
  })
};
</script>
