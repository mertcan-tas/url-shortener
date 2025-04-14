import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import { useAuthStore } from '@/plugins/stores/auth';

import NotFound404 from '@/views/errors/NotFound404.vue'

import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'

import DashboarView from '@/views/shortener/DashboarView.vue'

const router = createRouter({
  linkActiveClass: 'nav-link active',
  linkExactActiveClass: 'nav-link',
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboarView,
      meta: { requiresAuth: true }
    },
    {
      path: '/shorten-url',
      name: 'shorten-url',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/auth/login',
      name: 'login',
      component: LoginView,
      meta: { guest: true }
    },
    {
      path: '/auth/register',
      name: 'register',
      component: RegisterView,
      meta: { guest: true }
    },
    {
      path: '/:catchAll(.*)',
      name: 'notFound',
      component: NotFound404,
    }
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Giriş yapmış kullanıcılar için guest route kontrolü
  if (to.meta.guest && authStore.isLoggedIn) {
    next({ name: 'dashboard' })
    return
  }

  // Erişim kontrolü gereken route'lar için
  if (to.meta.requiresAuth) {
    if (authStore.isLoggedIn) {
      next()
    } else {
      // Giriş yapmamış kullanıcıları login sayfasına yönlendir
      next({ name: 'login' })
    }
  } else {
    next()
  }
})

export default router
