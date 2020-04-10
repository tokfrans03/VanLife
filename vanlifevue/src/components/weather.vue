<template>
  <v-card class="ma-4" color="grey darken-4">
    <v-list-item two-line>
      <v-list-item-content>
        <v-list-item-title class="headline">{{$store.state.stad}}</v-list-item-title>
        <v-list-item-subtitle>{{$store.state.weather.dayOfWeek}}, {{$store.state.weather.cloudCoverPhrase}}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <span class="display-3 mx-4">{{$store.state.weather.temperature}}&deg;C</span>

    <v-row align="start" justify="space-around">
      <v-col cols="10">
        <span class="display-3 mx-4">{{Math.round(($store.state.weather.windSpeed / 3.6 ) * 10 )/10 }} m/s</span>
        <span class="display-2 mx-4">{{$store.state.weather.windDirectionCardinal}}</span>
      </v-col>
      <v-col>
        <v-icon class="ma-4" :style="winddir()">mdi-arrow-up</v-icon>
      </v-col>
      <!-- <v-col>
        <v-list-item>
          <v-list-item-icon>
            <v-icon>mdi-cloud-download</v-icon>
          </v-list-item-icon>
          <v-list-item-subtitle>48%</v-list-item-subtitle>
        </v-list-item>
      </v-col>-->
    </v-row>

    <v-divider></v-divider>

    <v-card-actions >
      <v-btn text :href="`https://www.smhi.se/q/${$store.state.stad}`" class="display-1">
        SMHI
        <v-icon class="ml-2">mdi-open-in-new</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from "axios";
import { mapMutations } from "vuex";

export default {
  data() {
    return {};
  },
  created() {

  },
  methods: {
    ...mapMutations({
      Get_weather: "Get_weather" // map `this.add()` to `this.$store.commit('increment')`
    }),
    winddir() {
      return (
        "transform: rotate(" +
        (this.$store.state.weather.windDirection + 180) +
        "deg) scale(4);;"
      );
    }
  }
};
</script>