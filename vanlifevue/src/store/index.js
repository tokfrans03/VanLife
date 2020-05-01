import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";
import moment from "moment";
var geo = require('html5-geolocation')();

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    ver: "1.4.8",
    BackendUrl: "https://192.168.0.97:8000/",
    snac: false,
    snac_text: "",
    snac_color: "",
    config: {},
    retry: false,
    personer: [],
    Get_loading: false,
    stad: "Västerås",
    geo: "33.74,-84.39",
    weather: {},
    updateavailable: false,
    updateinfo: {},
    updateurl: "",
    time: "",
    load: false,
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
            state.snac_text = "Konfig laddad";
            state.snac_color = "success"
            state.snac = true;
          }
          state.retry = false;
          state.personer = []
          state.config.notif.forEach(person => {
            state.personer.push(person.name);
          });
          store.commit('Get_geo')
          store.commit('check_update', errors)
          

        })
        .catch(error => {
          if (verbose | errors) {
            state.snac_text = error + " Är Pi:en på?";
            state.snac_color = "error";
            state.snac = true;
          }
          state.retry = true;
          state.Get_loading = false
        });
    },
    Send_location: (state) => {
      let data = {
        action: "location",
        value: state.geo
      }
      axios.post(state.BackendUrl, data)
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
          state.snac_text = error;
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
      geo.get(function (err, position) {
        if (!err) {
          console.log('Position is:', position);
          state.geo = `${position.coords.latitude},${position.coords.longitude}`;
          localStorage.setItem('Geo', state.geo)
          store.commit('Get_city')
          store.commit('Send_location')
        } else {
          console.log('Position okänd:', position);
          let geo = localStorage.getItem('Geo');
          state.geo = geo
          store.commit('Get_city')
          state.snac_text = 'Position okänd:' + String(err.message) + " Använder: " + geo;
          state.snac_color = "error"
          state.snac = true;
          state.Get_loading = false;
        }
      });
    },
    Get_city: (state) => {
      let lat = state.geo.split(",")[0]
      let long = state.geo.split(",")[1]
      console.log(lat, long)
      let url = `https://locationiq.org/v1/reverse.php?key=d93c7305de485e&lat=${lat}&lon=${long}&format=json`;
      axios
        .get(url)
        .catch(error => {
          state.snac_text = error;
          state.snac_color = "error"
          state.snac = true;
          state.Get_loading = false;
        })
        .then(response => {
          if ("city" in response.data.address) {
            state.stad = response.data.address.city
          } else {
            state.stad = response.data.display_name.split(", ")[1]
          }
          store.commit('Get_weather')
        });
    },
    check_update: (state, verbose) => {
      let url =
        "https://api.github.com/repos/tokfrans03/VanLife/releases/latest";
      axios
        .get(url)
        .catch(error => {
          state.snac_text = error;
          state.snac_color = "error";
          state.snac = true;
          state.load = false;
        })
        .then(response => {
          state.load = false;
          if (response.data.tag_name != state.ver) {
            state.snac_text =
              "Version " + response.data.tag_name + " tillgänglig!";
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
            if (verbose) {
              state.snac_text = "Senaste version installerad";
              state.snac_color = "success";
              state.snac = true;
            }
          }
        });
    },
  },
  actions: {},
  modules: {}
})

export default store