export default {
  state: {
    daysTable: null
  },
  mutations: {
    setDaysTable (state, daysTable) {
      state.daysTable = daysTable;
    }
  },
  actions: {
    fillDaysTable ({ commit }, payload) {
      commit('setDaysTable', payload);
    }
  },
  getters: {
    daysTable (state) {
      return state.daysTable;
    }
  }
};
