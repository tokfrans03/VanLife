<template>
  <v-app>
    <v-card>
      <v-card-title primary-title>
        <div>
          <h3 class="headline mb-0">Dashboard</h3>
        </div>
      </v-card-title>
      <weather/>
    </v-card>
  </v-app>
</template>

<script>
import weather from "@/components/weather";

export default {
  name: "Dashboard",

  components: {
    weather
  }
};
</script>
