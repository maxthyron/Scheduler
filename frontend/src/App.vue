<template>
  <div id="app">
    <header>
      <nav class="navbar navbar-light bg-dark">
        <router-link to='/' class="navbar-brand text-light col-9"
          style="font-family: Menlo; font-size: 26px">Scheduler</router-link>
        <div class="options mr-3">
          <div v-if="checkUser">
            <span class="btn btn-dark disabled">{{ getUname }}</span>
              <router-link class="btn btn-dark btn-lg" to="/logout" @click.native="logout">Log out</router-link>
          </div>
          <div v-else>
            <router-link class="btn btn-dark btn-lg" to="/register">Sign up</router-link>
            <router-link class="btn btn-dark btn-lg" to="/login">Log in</router-link>
          </div>
        </div>
      </nav>
    </header>

    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    getUname () {
      return this.$store.getters.getUname
    },
    checkUser () {
      return this.$store.getters.checkUser
    }
  },
  methods: {
    logout () {
      this.$store.dispatch("logout")
    }
  }
}
</script>

<style>
</style>
