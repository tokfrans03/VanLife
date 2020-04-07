<template>
  <v-card class="mx-10" max-width="400">
    <v-list-item two-line>
      <v-list-item-content>
        <v-list-item-title class="headline">{{$store.state.stad}}</v-list-item-title>
        <v-list-item-subtitle>{{$store.state.weather.dayOfWeek}}, 12:30 PM, {{$store.state.weather.cloudCoverPhrase}}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-card-text>
      <v-row align="center">
        <v-col class="display-3" cols="6">{{$store.state.weather.temperature}}&deg;C</v-col>
      </v-row>
    </v-card-text>

    <v-list-item>
      <v-list-item-icon>
        <v-icon>mdi-send</v-icon>
      </v-list-item-icon>
      <v-list-item-subtitle>{{$store.state.weather.windSpeed}} m/s</v-list-item-subtitle>
    </v-list-item>

    <v-list-item>
      <v-list-item-icon>
        <v-icon>mdi-cloud-download</v-icon>
      </v-list-item-icon>
      <v-list-item-subtitle>48%</v-list-item-subtitle>
    </v-list-item>


    <v-divider></v-divider>

    <v-card-actions href="https://www.smhi.se/">
      <v-btn text>SMHI <v-icon>mdi-open-in-new</v-icon></v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
    };
  },
  mounted() {
    this.Get();
  },
  methods: {
    Get() {
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
          console.log(response.data)
          this.$store.state.weather = response.data;
        });
    }
  }
};
</script>