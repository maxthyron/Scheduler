import router from '../router'

import WebService from '../WebService'

export default {
  state: {
    is_authenticated: !!localStorage.getItem("token"),
    username: localStorage.getItem("username"),
    error: null
  },
  mutations: {
    setUserStatus (state, payload) {
      state.is_authenticated = payload
    },
    setUserName (state, payload) {
      state.username = payload
    },
    setError (state, payload) {
      state.error = payload
    }
  },
  actions: {
    userErrorOccurred({commit}, payload) {
      commit('setError', payload)
    },
    signup ({commit}, {uname, password}) {
      var obj = {
        'username': uname,
        'password': password
      }
      WebService.post('users', obj).then(ok => {
        console.log(ok)
        if (ok.data.error == null) {
          localStorage.setItem("token", "true")
          localStorage.setItem("username", uname)
          commit('setUserStatus', true)
          commit('setUserName', uname)
          commit('setError', null)
          router.push('/')
        } else {
          commit('setError', ok.data.error)
        }
      },
      err => {
        commit('setError', err.message)
      })
    },
    login ({commit}, {uname, password}) {
      var obj = {
        'password': password,
      }
      WebService.post('users/'+uname, obj).then(ok => {
        console.log(ok)
        if(ok.data.error == null) {
          localStorage.setItem("token", "true")
          localStorage.setItem("username", uname)
          commit('setUserStatus', true)
          commit('setUserName', uname)
          commit('setError', null)
          router.push('/')
        } else {
          commit('setError', ok.data.error)
        }
      },
      err => {
        console.log(err.message)
        commit('setError', err.message)
      })
    },
    logout ({commit}) {
      localStorage.removeItem("token")
      localStorage.removeItem("username")
      commit('setUserStatus', false)
    }
  },
  getters: {
    checkUser (state) {
      return state.is_authenticated
    },
    getUname (state) {
      return state.username
    },
    isUserErr (state) {
      return state.error != null
    },
    getUserErr (state) {
      return state.error
    }
  }
}
