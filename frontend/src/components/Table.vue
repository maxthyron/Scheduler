<template>
  <div class="table" role="tablist">
    <TableDay :day="day" :times-table="timesTable" v-for="day in daysTable" :key="day.id" />
  </div>
</template>

<script>
import TableDay from '@/components/TableDay';
import { requestsMixin } from '@/mixins/requestsMixin';

export default {
  name: 'Table',
  mixins: [requestsMixin],
  components: {
    TableDay
  },
  data () {
    return {
      daysTable: [],
      timesTable: []
    }
  },
  mounted () {
    this.getDaysTable()
      .then(response => (this.daysTable = response.data))
      .catch(e => (this.error = e));
    this.getTimesTable()
      .then(response => (this.timesTable = response.data));
  }
}
</script>

<style scoped>

</style>
