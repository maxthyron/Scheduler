import axios from 'axios';
import Vue from 'vue';

const BACKEND_URL = process.env.VUE_APP_BACKEND_URL || 'http://127.0.0.1:8000';

export const requestsMixin = Vue.mixin({
  methods: {
    getDaysTable () {
      return axios.get(`${BACKEND_URL}/api/schedule_days`);
    },
    getTimesTable () {
      return axios.get(`${BACKEND_URL}/api/schedule_times`);
    },
    getAuditoriumsTable (dayId, timeId) {
      return axios.get(`${BACKEND_URL}/api/table`, {
        params: {
          dayId,
          timeId
        }
      })
    }
  }
});
