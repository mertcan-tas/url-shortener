import axios from "axios"
import router from "./plugins/router"
import { useAuthStore } from "./plugins/stores/auth"

const client = axios.create({
  baseURL: "http://localhost:8000/api/",
  headers: {
    "Content-Type": "application/json",
  },
})

client.interceptors.request.use(
  (config) => {
    let token = localStorage.getItem("accessToken") || null

    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`
    } else {
      delete config.headers["Authorization"]
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

client.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()

      if (router.currentRoute.value.name === "login") {
        return Promise.reject(error)
      }
      router.push({ name: "login" })
    }
    return Promise.reject(error)
  }
)

export default client