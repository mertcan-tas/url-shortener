// src/stores/auth.js
/**
 * Authentication store using Pinia
 * Handles user authentication state and related operations
 */
import { defineStore } from 'pinia'
import userService from "@/services/api-service"

export const useAuthStore = defineStore('auth', {
  state: () => {
    // Initialize state from localStorage if available
    const token = localStorage.getItem("accessToken")
    const cachedUserData = JSON.parse(localStorage.getItem("userData") || "{}")
    return {
      user: {
        loggedIn: !!token,
        name: cachedUserData.name || "",
        surname: cachedUserData.surname || "",
        accessToken: token || null,
        lastFetched: cachedUserData.lastFetched || null
      }
    }
  },
  
  getters: {
    /**
     * Check if user is logged in
     * @returns {Boolean}
     */
    isLoggedIn: (state) => state.user.loggedIn,
    
    /**
     * Get current user data
     * @returns {Object}
     */
    userData: (state) => state.user,

    /**
     * Check if user data needs to be refreshed
     * @returns {Boolean}
     */
    shouldRefreshUserData: (state) => {
      if (!state.user.lastFetched) return true
      const now = new Date().getTime()
      const lastFetch = new Date(state.user.lastFetched).getTime()
      // 5 dakikadan eski veriyi yenile
      return (now - lastFetch) > 5 * 60 * 1000
    }
  },
  
  actions: {
    /**
     * Handle successful login
     * @param {String} token - Access token from API
     */
    loginSuccessful(token) {
      this.user.loggedIn = true
      this.user.accessToken = token
      localStorage.setItem("accessToken", token)
    },
    
    /**
     * Handle user logout
     */
    logout() {
      this.user.loggedIn = false
      this.user.accessToken = null
      this.user.name = ""
      this.user.surname = ""
      this.user.lastFetched = null
      localStorage.removeItem("accessToken")
      localStorage.removeItem("userData")
    },
    
    /**
     * Set user profile data
     * @param {Object} userInfo - User profile information
     */
    setUserData(userInfo) {
      this.user.name = userInfo.name
      this.user.surname = userInfo.surname
      this.user.lastFetched = new Date().toISOString()
      
      // Cache user data in localStorage
      localStorage.setItem("userData", JSON.stringify({
        name: userInfo.name,
        surname: userInfo.surname,
        lastFetched: this.user.lastFetched
      }))
    },
    
    /**
     * Login request to API
     * @param {Object} payload - Login credentials
     * @returns {Promise}
     */
    async loginRequest(payload) {
      try {
        const response = await userService.login(payload)
        if (response.data && response.data.access) {
          this.loginSuccessful(response.data.access)
          await this.getUserData() // Fetch user details after successful login
          return Promise.resolve(response.data)
        }
        return Promise.reject(new Error('Invalid response format'))
      } catch (error) {
        this.logout() // Clear state on failed login
        return Promise.reject(error)
      }
    },
    
    /**
     * Register new user
     * @param {Object} payload - Registration data
     * @returns {Promise}
     */
    async registerRequest(payload) {
      try {
        const response = await userService.register(payload)
        if (response.data && response.data.access) {
          this.loginSuccessful(response.data.access)
          await this.getUserData() // Fetch user details after successful registration
        }
        return Promise.resolve(response.data)
      } catch (error) {
        return Promise.reject(error)
      }
    },
    
    /**
     * Fetch user details
     * @returns {Promise}
     */
    async getUserData() {
      try {
        // Eğer veri taze ise API'ye istek atma
        if (!this.shouldRefreshUserData) {
          return Promise.resolve(this.user)
        }

        const response = await userService.userDetail()
        this.setUserData(response.data)
        return Promise.resolve(response.data)
      } catch (error) {
        this.logout() // Clear state if user details can't be fetched
        return Promise.reject(error)
      }
    },
    
    /**
     * Handle logout request
     * @returns {Promise}
     */
    async logoutRequest() {
      try {
        this.logout()
        return Promise.resolve()
      } catch (error) {
        return Promise.reject(error)
      }
    }
  }
})