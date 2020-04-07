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
        <span class="display-3 mx-4">{{$store.state.weather.windSpeed}} m/s</span>
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

    <v-card-actions href="https://www.smhi.se/">
      <v-btn text>
        SMHI
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {};
  },
  mounted() {
    this.Get_weather();
  },
  methods: {
    Get_weather() {
      let url =
        "https://api.weather.com/v3/wx/observations/current?geocode=" +
        "33.74,-84.39" +
        "&units=m&language=sv&format=json&apiKey=" +
        this.$store.state.config.weather.key;
      axios
        .get(url)
        .catch(error => {
          this.$store.state.snac_text = "Unable to get weather";
          this.$store.state.snac = true;
        })
        .then(response => {
          console.log(response.data);
          this.$store.state.weather = response.data;
        });
    },
    winddir() {
      return (
        "transform: rotate(" +
        this.$store.state.weather.windDirection +
        "deg) scale(4);;"
      );
    }
  }
};
</script>