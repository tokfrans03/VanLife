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
    Get_loading: false
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
  },
  actions: {},
  modules: {}
})

export default store