import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";
import moment from "moment";
var geolocation = require("geolocation");

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
    weather: {},
    ver: "0.9",
    updateavailable: false,
    updateinfo: {},
    updateurl: "",
    time: "",
    load: false
  },
  mutations: {
    Get: (state, verbose, errors) => {
      state.Get_loading = true
      // console.log("GETTOINGG")
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
          store.commit('Get_geo')

        })
        .catch(error => {
          if (verbose | errors) {
            state.snac_text = "Unable to get config, is the server running?";
            state.snac_color = "error";
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
        state.config.creds.weather;
      axios
        .get(url)
        .catch(error => {
          state.snac_text = "Unable to get weather";
          state.snac = true;
          state.Get_loading = false;
        })
        .then(response => {
          state.weather = response.data;
          state.Get_loading = false;
          // console.log("GGOOMGNGN DONE")
        });
    },
    Get_geo: (state) => {
      geolocation.getCurrentPosition(function (err, position) {
        if (err) throw err;
        // console.log(position);
        state.geo = `${position.coords.latitude},${position.coords.longitude}`;
        let url = `https://locationiq.org/v1/reverse.php?key=d93c7305de485e&lat=${position.coords.latitude}&lon=${position.coords.longitude}&format=json`;
        axios
          .get(url)
          .catch(error => {
            state.snac_text = "Unable to reach network";
            state.snac = true;
            state.Get_loading = false;
          })
          .then(response => {
            state.stad = response.data.address.city
            store.commit('Get_weather')
          });
      });
    },
    check_update: (state) => {
      let url =
        "https://api.github.com/repos/tokfrans03/VanLife/releases/latest";
      axios
        .get(url)
        .catch(error => {
          state.snac_text = "Unable to reach network";
          state.snac = true;
          state.load = false;
        })
        .then(response => {
          state.load = false;
          if (response.data.tag_name != state.ver) {
            state.snac_text =
              "Version " + response.data.tag_name + " available!";
            state.snac_color = "success";
            state.snac = true;
            state.updateavailable = true;
            state.updateinfo = response.data;
            moment.locale("sv");
            state.time =
              moment(state.updateinfo.published_at).format("lll") +
              ", " +
              moment(state.updateinfo.published_at).fromNow();
            axios.get(response.data.assets_url).catch(error => {
              state.snac_text = error;
              state.snac = true;
              state.load = false;
            }).then(response => {
              state.updateurl = response.data[0].browser_download_url
            })
          } else {
            state.snac_text = "No new updates found";
            state.snac_color = "success";
            state.snac = true;
          }
        });
    },
  },
  actions: {},
  modules: {}
})

export default store