import { mapState, mapActions } from 'pinia'
import { useAuthStore } from '@/plugins/stores/auth'; // Store yolunuzu kontrol edin

// Düzeltme: export default kullanıyoruz
export default {
  computed: {
    ...mapState(useAuthStore, ['user']),
    
    isLoggedIn() {
      return this.user?.loggedIn || false
    }
  },
  methods: {
    ...mapActions(useAuthStore, ['logoutRequest']),
    
    async logout() {
      try {
        await this.logoutRequest()
        this.$router.push({ name: 'login' }) // Kendi route ayarlarınıza göre düzenleyin
      } catch (error) {
        console.error('Çıkış hatası:', error)
        // İsteğe bağlı: Hata bildirimi ekleyebilirsiniz
      }
    }
  }
}