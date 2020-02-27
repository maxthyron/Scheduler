import Vue from 'vue'
import Vuex from 'vuex'

import daysTable from './daysTable';
import timesTable from './timesTable';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    error: null
  },
  mutations: {
    setError (state, error) {
      state.error = error
    }
  },
  actions: {
    gotError ({ commit }, error) {
      commit('setError', error)
    }
  },
  modules: {
    daysTable,
    timesTable
  },
  getters: {
    getError (state) {
      return state.error;
    }
  }
})
