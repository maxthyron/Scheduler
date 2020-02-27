import axios from 'axios';
import Vue from 'vue';

const BACKEND_URL = process.env.VUE_APP_BACKEND_URL || 'http://127.0.0.1:8000';

const router = axios.create({
  baseURL: BACKEND_URL
});

export const requestsMixin = Vue.mixin({
  methods: {
    getDaysTable () {
      return router.get('/api/schedule_days');
    },
    getTimesTable () {
      return router.get('/api/schedule_times');
    },
    getAuditoriumsTable (dayId, timeId) {
      return router.get('/api/table', {
        params: {
          dayId,
          timeId
        }
      })
    }
  }
});
