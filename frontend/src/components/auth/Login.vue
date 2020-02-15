<template>
  <section>
    <div class="container mt-4">
      <form>
        <div class="form-group">
          <label for="username">Username*</label>
          <input type="text" class="form-control" placeholder="Username"
                v-model.trim="$v.username.$model"
                @keyup.enter="check_fields"
                :class="{ 'is-invalid' : $v.username.$error }">
        </div>
        <div class="form-group">
          <label for="password">Password*</label>
          <input type="password" class="form-control" placeholder="Password"
                v-model.trim="$v.password.$model"
                @keyup.enter="check_fields"
                :class="{ 'is-invalid' : $v.password.$error }">
        </div>
        <div class="form-group">
          <button class="btn btn-outline-dark" type="submit" @click="check_fields">Log in</button>
        </div>
        <div class="form-group">
          <div v-if="isErr" class="alert alert-danger" role="alert">
            {{ getErr }}
          </div>
        </div>
      </form>
      <div class="border-top pt-3">
        <small class="text-muted">Create an account? <router-link class="ml-2" to="/register">Sign up</router-link></small>
      </div>
    </div>
  </section>
</template>

<script>
import { required } from 'vuelidate/lib/validators'
export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  validations: {
    username: {
      required
    },
    password: {
      required
    }
  },
  computed: {
    isErr () {
      return this.$store.getters.isUserErr
    },
    getErr () {
      return this.$store.getters.getUserErr
    }
  },
  created () {
    this.$store.dispatch('userErrorOccurred', null)
  },
  methods: {
    check_fields () {
      this.$v.$touch()
      if(this.$v.$invalid) {
        this.$store.dispatch('userErrorOccurred', 'All fields required!')
      } else {
        var user_data = {
          uname: this.$v.username.$model,
          password: this.$v.password.$model
        }
        this.$store.dispatch('login', user_data)
      }
    }
  }
}
</script>

<style scoped>
</style>
