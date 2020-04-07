<template>
  <div>
    <v-toolbar dark>
      <v-toolbar-title>Vanlife</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-toolbar-items>
        <v-btn v-for="(link, i) in links" :key="i" :to="link.path">{{link.name}}</v-btn>
      </v-toolbar-items>
    </v-toolbar>
  </div>
</template>

<script>
import paths from "@/router/paths";

export default {
  data: () => ({}),
  computed: {
    links() {
      return paths;
    }
  }
};
</script>