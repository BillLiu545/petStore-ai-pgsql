import { createRouter, createWebHistory } from 'vue-router'
import login from '../components/login.vue'
import create from '../components/create.vue'
import menu from '../components/menu.vue'
import mainpage from '@/components/mainpage.vue'

const routes = [
    {path: '/', component: login},
    {path: '/create', component: create},
    {path: '/menu', component: mainpage},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router