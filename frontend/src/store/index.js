import Vue from 'vue'
import Vuex from 'vuex'

import user from './user'
import table from './table'
import audit from './audit'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user,
    table,
    audit
  }
})
