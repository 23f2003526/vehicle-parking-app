// src/stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isAdmin: false,
    details: {},
    isLoggedIn: false
  }),

  actions: {
    setUserDetails(details) {
      this.details = details
      this.isAdmin = details.role === 'admin'
      this.isLoggedIn = true
      // console.log('I am admin')
    },
    logout() {
      this.details = {}
      this.isAdmin = false
      this.isLoggedIn = false
      // console.log('I am not admin')
    }
  }
})