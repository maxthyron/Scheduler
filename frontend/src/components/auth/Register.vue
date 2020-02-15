<template>
  <section>
    <div class="container mt-4">
      <form>
        <div class="form-group"> <!--:class="{ 'is-invalid': $v.username.$error }"-->
          <label for="username">Username*</label>
          <input type="text" class="form-control" 
                placeholder="Username"
                v-model.trim="$v.username.$model"
                @keyup.enter="check_fields"
                :class="{ 'is-invalid': $v.username.$error }">
          <small class="form-text" 
            :class="$v.username.$error ? 'invalid-feedback' : 'text-muted'">
            Required. 3-15 characters of fewer. Letters, digits, and @/./+/-/_ only.
          </small>
        </div>
        <div class="form-group">
          <label for="password">Password*</label>
          <input type="password" class="form-control"
                placeholder="Password"
                v-model.trim="$v.password.$model"
                @keyup.enter="check_fields"
                :class="{ 'is-invalid': $v.password.$error }">
            <small class="form-text" 
              :class="$v.password.$error ? 'invalid-feedback' : 'text-muted'">
              <div class="container">
                <td>
                  <tr>- Your password can't be too similar to your other personal information.</tr>
                  <tr>- Your password must contain at least 6 characters.</tr>
                  <tr>- Your password can't be a commonly used password.</tr>
                  <tr>- Your password can't be entirely numeric</tr>
                </td>
              </div>
          </small>
        </div>
        <div class="form-group">
          <label for="password">Password confirmation*</label>
          <input type="password" class="form-control"
                placeholder="Password"
                v-model.trim="$v.password_conf.$model"
                @keyup.enter="check_fields"
                :class="{ 'is-invalid': $v.password_conf.$error }">
          <small class="form-text text-muted" v-if="!$v.password_conf.$error">Repeat your password.</small>
          <div class="invalid-feedback" v-if="!$v.password_conf.$sameAsPassword">Passwords must be identical.</div>
        </div>
        <div class="form-group">
          <button class="btn btn-outline-dark" type="submit" @click="check_fields">Sign up</button>
        </div>
        <div class="form-group">
          <div v-if="isErr" class="alert alert-danger" role="alert">
            {{ getErr }}
          </div>
        </div>
      </form>
      <div class="border-top pt-3">
        <small class="text-muted">Already have an account? <router-link class="ml-2" to="/login">Sign in</router-link></small>
      </div>
    </div> 
  </section>
</template>

<script>
import { required, minLength, sameAs, helpers, maxLength } from 'vuelidate/lib/validators'

const alpha_name = helpers.regex('alpha', /^[A-Za-z\d@.+-_]*$/)
const alpha_pass = helpers.regex('alpha', /(?!^\d+$)^.+$/)

export default {
  data () {
    return {
    username: '',
    password: '',
    password_conf: ''
    }
  },
  validations: {
    username: {
      required,
      alpha_name,
      minLength: minLength(3),
      maxLength: maxLength(15)
    },
    password: {
      required,
      alpha_pass,
      minLength: minLength(6),
      maxLength: maxLength(50)
    },
    password_conf: {
      sameAsPassword: sameAs('password')
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
      if (this.$v.$invalid)
        this.$store.dispatch('userErrorOccurred', 'Fields are incorrect!')
      else {
        var user_data = {
          uname: this.$v.username.$model,
          password: this.$v.password.$model
        }
        this.$store.dispatch('signup', user_data)
      }
        
    }
  }
}
</script>

<style scoped>
</style>

