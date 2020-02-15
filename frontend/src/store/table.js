import WebService from '../WebService'

export default {
  state: {
    times: [
      {
        'id': 0,
        'value': '8:30-10:05'
      },
      {
        'id': 1,
        'value': '10:15-11:50'
      },
      {
        'id': 2,
        'value': '12:00-13:35'
      },
      {
        'id': 3,
        'value': '13:50-15:25'
      },
      {
        'id': 4,
        'value': '15:40-17:15'
      },
      {
        'id': 5,
        'value': '17:25-19:00'
      },
      {
        'id': 6,
        'value': '19:10-20:45'
      }
    ],
    table: [
      {
        'day': 'Monday',
        'array': [
          {
            'state': 'free',
            'array': [
              {
                'time': '0',
                'classes': [
                  {'id': '513л'}
                ]
              },
              {
                'time': '1',
                'classes': [
                  {'id': '611л'}
                ]
              }
            ]
          },
          {
            'state': 'occupied',
            'array': [
              {
                'time': '0',
                'classes': [
                  {'id': '813л'}
                ]
              },
              {
                'time': '1',
                'classes': [
                  {'id': '991'}
                ]
              }
            ]
          },
          {
            'state': 'reserved',
            'array': [
              {
                'time': '0',
                'classes': [
                  {
                    'id': '666л',
                    'user_id': 'max'
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        'day': 'Tuesday',
        'array': [
          {
            'state': 'free',
            'array': [
              {
                'time': '0',
                'classes': [
                  {'id': '1111л'}
                ]
              }
            ]
          },
          {
            'state': 'occupied',
            'array': [
              {
                'time': '0',
                'classes': [
                  {'id': '111л'}
                ],
              }
            ]
          },
          {
            'state': 'reserved',
            'array': [
              {
                'time': '0',
                'classes': [
                  {
                    'id': '6666л',
                    'user_id': 'max'
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  mutations: {
      setTable (state, payload) {
        state.table = payload
      }
  },
  actions: {
    fillTable ({commit}) {
      WebService.get('table').then(ok =>
        commit('setTable', ok.data)
      )
    }
  },
  getters: {
    table (state) {
      return state.table
    },
    times (state) {
      return state.times
    }
  }
}
