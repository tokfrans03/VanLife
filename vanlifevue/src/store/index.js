import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    BackendUrl: "http://localhost:8000/",
    snac: false,
    snac_text: "",
    config: {},
    retry: false,
    personer: [],
    Get_loading: false,
    stad: "Västerås",
    geo: "33.74,-84.39",
    weather:{
    }
  },
  mutations: {
    Get: (state, verbose) => {
      state.Get_loading = true
      axios
        .get(state.BackendUrl)
        .then(response => {
          // console.log(response);
          state.config = response.data.value.config;
          if (verbose) {
            state.snac_text = "Loaded config";
            state.snac = true;
          }
          state.retry = false;
          state.personer = []
          state.config.notif.forEach(person => {
            state.personer.push(person.name);
          });
          state.Get_loading = false
        })
        .catch(error => {
          if (verbose) {
            state.snac_text = "Unable to get config";
            state.snac = true;
          }
          state.retry = true;
          state.Get_loading = false
        });
    },
    Get_weather: (state) => {
      let url =
        "https://api.weather.com/v3/wx/observations/current?geocode=" +
        state.geo +
        "&units=m&language=sv&format=json&apiKey=" +
        state.config.weather.key;
      axios
        .get(url)
        .catch(error => {
          state.snac_text = "Unable to get weather";
          state.snac = true;
        })
        .then(response => {
          state.weather = response.data;
        });
    },
  },
  actions: {},
  modules: {}
})

export default store