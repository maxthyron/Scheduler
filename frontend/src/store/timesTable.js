export default {
  state: {
    timesTable: null
  },
  mutations: {
    setTimesTable (state, timesTable) {
      state.timesTable = timesTable;
    }
  },
  actions: {
    fillTimesTable ({ commit }, payload) {
      commit('setTimesTable', payload);
    }
  },
  getters: {
    timesTable (state) {
      return state.timesTable;
    }
  }
};
