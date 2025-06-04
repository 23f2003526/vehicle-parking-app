import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue';
import LandingPageView from '@/views/LandingPageView.vue';
import SignupView from '@/views/SignupView.vue';
import NotFoundView from '@/views/NotFoundView.vue';
import DashboardView from '@/views/DashboardView.vue';
import ParkingLotView from '@/views/ParkingLotView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing-page',
      component: LandingPageView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/:patchMatch(.*)*',
      name: 'not-found',
      component: NotFoundView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true}
    },
    {
      path: '/admin/lots/:id',
      name: 'parking-lot-view',
      component: ParkingLotView,
      meta: { requiresAuth: true}
    },
  ],
})

export default router
