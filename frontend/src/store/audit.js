import WebService from '../WebService'

export default {
  state: {
    id: '',
    day_id: '',
    time_id: '',
    username: '',
    groups: null,
    form: '',
    subject: null,
    error: ''
  },
  mutations: {
    setForm (state, payload) {
      state.form = payload
    },
    setGroups (state, payload) {
      state.groups = payload
    },
    setAudit (state, payload) {
      state.id = payload
    },
    setDay (state, payload) {
      state.day_id = payload
    },
    setUsername (state, payload) {
      state.username = payload
    },
    setTime (state, payload) {
      state.time_id = payload
    },
    setSubject (state, payload) {
      state.subject = payload
    },
    setAudError (state, payload) {
      state.error = payload
    }
  },
  actions: {
    auditErrorOccurred({commit}, payload) {
      commit('setAudError', payload)
    },
    getAuditData ({commit}, {time, day, audit}) {
      commit('setTime', time)
      commit('setAudit', audit)
      commit('setDay', day)
      WebService.get('classes/'+audit+'?aud_time='+time+'&aud_day='+day).then(ok => {
        if (ok.data.error == null) {
          commit('setForm', ok.data.form)
          commit('setUsername', ok.data.username)
          commit('setSubject', ok.data.subject)
          commit('setGroups', ok.data.groups)
          commit('setAudError', null)
        } else {
          commit('setAudError', ok.data.error)
        }
      },
      err => {
        commit('setAudError', err.message)
      })
    },
    reserve ({commit}, {uname, time, day, audit}) {
      var obj = {
        'username': uname,
        'time': time,
        'day': day,
      }
      console.log(obj)
      WebService.post('classes/'+audit+'/reserve', obj).then(ok => {
        if (ok.data.error == null) {
          commit('setForm', 'occupied_by_user')
          commit('setSubject', null)
          commit('setGroups', null)
          commit('setAudError', null)
          commit('setUsername', uname)
        } else {
          commit('setAudError', ok.data.error)
        }
      },
      err => {
        commit('setAudError', err.message)
      })
    },
    cancelReservation ({commit}, {uname, time, day, audit}) {
      var obj = {
        'username': uname,
        'time': time,
        'day': day,
      }
      WebService.post('classes/'+audit+'/unreserve', obj).then(ok => {
        console.log(ok)
        if(ok.data.error == null) {
          commit('setForm', 'not_occupied')
          commit('setSubject', null)
          commit('setGroups', null)
          commit('setAudError', null)
          commit('setUsername', null)
        } else {
          commit('setAudError', ok.data.error)
        }
      },
      err => {
        console.log(err.message)
        commit('setAudError', err.message)
      })
    },
  },
  getters: {
    getAudUname (state) {
      return state.username
    },
    getAudDay (state) {
      return state.day_id
    },
    getAudTime (state) {
      return state.time_id
    },
    getAudId (state) {
      return state.id
    },
    getAudForm (state) {
      return state.form
    },
    getAudSubject (state) {
      return state.subject
    },
    getAudGroups (state) {
      return state.groups
    },
    getAudErr (state) {
      return state.error
    },
    isAudErr (state) {
      return state.error
    }
  }
}
