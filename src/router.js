import Vue from 'vue'
import Router from 'vue-router'

import Lectures from '@/components/Lectures'
import Lecture from '@/components/Lecture'
import Survey from '@/components/Survey'
import Login from '@/components/Login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Lectures
    },
    {
      path: '/lecture/:Lid',
      name: 'lecture',
      component: Lecture
    },
    {
      path: '/survey/:Sid',
      name: 'survey',
      component: Survey
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    }
  ]
})
