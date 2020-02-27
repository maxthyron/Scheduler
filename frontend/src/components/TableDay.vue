<template>
  <b-card no-body class="mb-1">
    <b-card-header header-tag="header" class="p-1" role="tab">
      <b-button v-b-toggle="'day_' + day.id" block href="#" variant="dark">{{ day.name }}</b-button>
    </b-card-header>
    <b-collapse :id="'day_' + day.id" accordion="days-accordion" role="tabpanel">
      <b-container style="height:340px;">
        <b-row class="no-gutters" style="height:340px;">
          <b-col cols="4">
            <b-button-group vertical class="w-100">
              <b-button @click='getAuditoriums(day, time)' :key="time.id"
                        v-for="time in timesTable">{{time['start_time']}}</b-button>
            </b-button-group>
          </b-col>
          <b-col>
            <b-container style="overflow-y: scroll; height:335px;" class="p-0">
              <TableAuditorium :auditoriums="auditoriums" />
            </b-container>
          </b-col>
        </b-row>
      </b-container>
    </b-collapse>
  </b-card>
</template>

<script>
import TableAuditorium from '@/components/TableAuditorium';
import { requestsMixin } from '@/mixins/requestsMixin';

export default {
  name: 'TableDay',
  components: { TableAuditorium },
  mixins: [requestsMixin],
  data () {
    return {
      auditoriums: []
    }
  },
  props: {
    day: {
      type: null,
      required: true
    },
    timesTable: {
      type: null,
      required: true
    }
  },
  methods: {
    getAuditoriums (day, time) {
      this.getAuditoriumsTable(day.id, time.id)
        .then(response => (this.auditoriums = response.data));
    }
  }
}
</script>

<style scoped>
</style>
