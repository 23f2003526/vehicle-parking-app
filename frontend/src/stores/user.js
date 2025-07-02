// src/stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    isAdmin: false,
    details: {}
  }),

  actions: {
    setUserDetails(details) {
      this.details = details
      this.isAdmin = details.role === 'admin'
    },
    logout() {
      this.details = {}
      this.isAdmin = false
    }
  }
})
