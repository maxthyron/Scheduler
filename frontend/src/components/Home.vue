<template>
  <div class="container mb-4">
    <div v-for="(item, key, index) in schedule_table">
      <h1> {{item.day}} </h1>
        <div class="accordion" role="tablist" id="table" v-for="(time, t_key, t_index) in times">
          <div class="card" role="tab">
            <div class="card-header" :id="time.value">
              <button class="btn btn-link collapsed" type="button" data-toggle="collapse"
                      :data-target="'#table-'+time.id+'-'+item.day">
                {{ time.value }}
              </button>
                <div :id="'table-'+time.id+'-'+item.day" class="collapse"
                      :aria-labelledby="'table-'+time.id+'-'+item.day" data-parent="#table"
                      v-for="(audit, audit_key, audit_index) in item.array" v-if="classesOnTime(audit, time.id)">
                  <div class="card-body row" v-for="(a, a_key, a_index) in audit.array" v-if="a.time == time.id">
                              <div v-for="num in a.classes" v-if="audit.state=='free'"
                                  class="col col-sm-2">
                                  <router-link class="btn btn-success btn-block mb-2" aria-expaneded="false" :to="{ name: 'classes', params: {aud_id: num.id}, query: {aud_time: time.id, aud_day: item.day}}">{{ num.id }}</router-link>
                              </div>
                              <div v-for="num in a.classes" v-if="audit.state=='reserved'"
                                  class="col col-sm-2">
                                  <router-link class="btn btn-primary btn-block mb-2" aria-expanded="false" :to="{ name: 'classes', params: {aud_id: num.id}, query: {aud_time: time.id, aud_day: item.day}}">{{ num.id }}</router-link>
                              </div>
                              <div v-for="num in a.classes" v-if="audit.state=='occupied'"
                                  class="col col-sm-2">
                                  <router-link class="btn btn-danger btn-block mb-2" aria-expanded="false" :to="{ name: 'classes', params: {aud_id: num.id}, query: {aud_time: time.id, aud_day: item.day}}">{{ num.id }}</router-link>
                              </div>
                  </div>
                </div>
            </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
    }
  },
  beforeCreate () {
    this.$store.dispatch('fillTable')
  },
  computed: {
    schedule_table () {
      return this.$store.getters.table
    },
    times () {
      return this.$store.getters.times
    }
  },
  methods: {
    classesOnTime: function(obj, t) {
      var result = false
      for (var i in obj['array']) {
        if (obj['array'][i]['time'] == t && obj['array'][i]['classes'].length != 0)
          result = true
      }
      return result
    }
  }
}
</script>

<style scoped>
</style>
