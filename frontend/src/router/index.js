import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue';
import LandingPageView from '@/views/LandingPageView.vue';
import SignupView from '@/views/SignupView.vue';
import NotFoundView from '@/views/NotFoundView.vue';
import DashboardView from '@/views/DashboardView.vue';
import ParkingLotView from '@/views/ParkingLotView.vue';
import CreateParkingLotView from '@/views/CreateParkingLotView.vue';
import EditParkingLotView from '@/views/EditParkingLotView.vue';
import UsersView from '@/views/UsersView.vue';
import BookingsView from '@/views/BookingsView.vue';
import AdminSummaryView from '@/views/AdminSummaryView.vue';
import UserSummaryView from '@/views/UserSummaryView.vue';
import EditProfileView from '@/views/EditProfileView.vue';

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
      meta: { requiresAuth: true},
    },
    {
      path: '/admin/lots/create',
      name: 'create-parking-lot-view',
      component: CreateParkingLotView,
      meta: { requiresAuth: true}
    },
    {
      path: '/admin/lots/:id/edit',
      name: 'edit-parking-lot-view',
      component: EditParkingLotView,
      meta: { requiresAuth: true}
    },
    {
      path: '/admin/users',
      name: 'users-view',
      component: UsersView,
      meta: { requiresAuth: true}
    },
      {
      path: '/admin/bookings',
      name: 'bookings-view',
      component: BookingsView,
      meta: { requiresAuth: true}
    },
    {
      path: '/admin/summary',
      name : 'admin-summary',
      component: AdminSummaryView,
      meta: {requiresAuth: true}
    },
    {
      path: '/summary',
      name : 'user-summary',
      component: UserSummaryView,
      meta: {requiresAuth: true}
    },
    {
      path: '/edit-profile',
      name : 'edit-profile',
      component : EditProfileView,
      meta : {requiresAuth: true}
    }
  ],
})

export default router
