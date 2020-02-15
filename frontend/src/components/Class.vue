<template>
<section class="container">
<div class="media mb-4">
  <div class="media-body">
    <h2 class="mt-4">
      Auditorium: {{ aud_id }}
    </h2>
    <div class="border-top pt-3">
      <h3 class="mt-2">
        <div v-if="form == 'occupied'">
          <p>Subject: {{ subject.name }} {{ subject.type }}</p>
          Occupied by:
          <span class="badge badge-dark" v-for="group in groups">{{ group }}</span>
        </div>
        <div v-else-if="form == 'occupied_by_user'">
          Occupied by:
          <span class="badge badge-dark">{{ aud_user }}</span>
        </div>
        <div v-else>
          Not occupied
        </div>
      </h3>
    </div>
    <div class="mt-4">
      <div v-if="form == 'not_occupied'">
        <div v-if="checkUser">
          <button class="btn btn-dark btn-lg" id="take_aud" @click="reserve">Occupy auditorium</button>
        </div>
        <div v-else>
          <button class="btn btn-secondary btn-lg disabled">Occupy auditorium</button>
          <div class="pt-3">
            <small class="text-muted">
              You need to be logged in to occupy this auditorium!
            <br>
                Have an account or want to create one? Then <router-link
                to="/login">log in</router-link> or <router-link
                to="/register">sign up</router-link>!
            </small>
          </div>
        </div>
      </div>
      <div v-else>
        <div v-if="checkUser && getUname == aud_user">
            <button class="btn btn-dark btn-lg" id="cancel_reserved" @click=canselReservation>Cancel reservation</button>
        </div>
      </div>
      <div class="mt-2 media-body">
        <div v-if="isAudErr" class="alert alert-danger" role="alert">
          {{ getAudErr }}
        </div>
      </div>
    </div>
  </div>
</div>
</section>
</template>

<script>
export default {
  props: ['aud_id'],
  data () {
    return {
    }
  },
  created () {
    var data = {
      time: this.$route.query.aud_time,
      day: this.$route.query.aud_day,
      audit: this.$props.aud_id
    }
    this.$store.dispatch('getAuditData', data)
  },
  computed: {
    aud_time () {
      return this.$route.query.aud_time
    },
    aud_day () {
      return this.$route.query.aud_day
    },
    aud_user () {
      return this.$store.getters.getAudUname
    },
    isAudErr () {
      return this.$store.getters.isAudErr
    },
    getAudErr () {
      return this.$store.getters.getAudErr
    },
    day () {
      return this.$store.getters.getAudDay
    },
    time () {
      return this.$store.getters.getAudTime
    },
    audit () {
      return this.$store.getters.getAudId
    },
    subject () {
      return this.$store.getters.getAudSubject
    },
    form () {
      return this.$store.getters.getAudForm
    },
    groups () {
      return this.$store.getters.getAudGroups
    },
    checkUser () {
      return this.$store.getters.checkUser
    },
    getUname () {
      return this.$store.getters.getUname
    }
  },
  methods: {
    reserve () {
      var data = {
        uname: this.$store.getters.getUname,
        time: this.$store.getters.getAudTime,
        day: this.$store.getters.getAudDay,
        audit: this.$store.getters.getAudId
      }
      this.$store.dispatch('reserve', data)
    },
    canselReservation () {
      var data = {
        uname: this.$store.getters.getUname,
        time: this.$store.getters.getAudTime,
        day: this.$store.getters.getAudDay,
        audit: this.$store.getters.getAudId
      }
      this.$store.dispatch('cancelReservation', data)
    },
  }
}
</script>

<style scoped>
</style>
