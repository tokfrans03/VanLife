<template>
  <v-card class="my-2">
    <v-card-title>{{ Title }}</v-card-title>
    <v-card-text>
      <v-row align="start" justify="space-around" no-gutters>
        <v-col>
          <span style="font-weight: bold; font-size: 550%; color: #FFFFFF">{{ Temp }}°C</span>
        </v-col>
        <v-col cols="auto">
          <v-icon class="mr-8" style="transform: scale(5);" v-if="Trend=='up'">mdi-arrow-top-right</v-icon>
          <v-icon class="mr-8" style="transform: scale(5);" v-if="Trend=='stable'">mdi-arrow-right</v-icon>
          <v-icon
            class="mr-8"
            style="transform: scale(5);"
            v-if="Trend=='down'"
          >mdi-arrow-bottom-right</v-icon>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "Temp",
  props: {
    Title: {
      type: String,
      required: true
    },
    Temp: {
      type: Number,
      required: true
    },
    Trend: {
      type: String,
      required: false
    }
  }
};
</script>

<style>
#arrow {
  transform: scale(3, 3);
}
</style>