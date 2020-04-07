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
  },
  mutations: {
    Get: (state) => {
      axios
        .get(state.BackendUrl)
        .then(response => {
          // console.log(response);
          state.config = response.data.value.config;
          state.snac_text = "Loaded config";
          state.snac = true;
          state.retry = false;
        })
        .catch(error => {
          state.snac_text = "Unable to get config";
          state.snac = true;
          state.retry = true;
        });
    },
  },
  actions: {
  },
  modules: {
  }
})

export default store