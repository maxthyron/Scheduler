import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Class from '@/components/Class'
import Login from '@/components/auth/Login'
import Register from '@/components/auth/Register'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/classes/:aud_id',
      name: 'classes',
      component: Class,
      props: true
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/logout',
      name: 'logout',
      redirect: '/'
    }
  ]
})
