<template>
  <BaseLayout>
    <v-container class="fill-height" fluid>
      <v-row justify="center" align="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title>Login</v-toolbar-title>
            </v-toolbar>
            
            <v-card-text>
              <v-form ref="form" @submit.prevent="login">
                <v-text-field
                  v-model="email"
                  label="E-mail"
                  class="mb-5 mt-4"
                  prepend-icon="mdi-email"
                  type="email"
                  required
                  :rules="emailRules"
                ></v-text-field>

                <v-text-field
                  v-model="password"
                  label="Password"
                  class="mb-5 mt-4"
                  prepend-icon="mdi-lock"
                  type="password"
                  required
                  :rules="passwordRules"
                ></v-text-field>

                <v-btn 
                  type="submit" 
                  color="primary" 
                  block
                  :loading="loading"
                >
                  Login
                </v-btn>
              </v-form>
            </v-card-text>

            <v-alert v-if="error" type="error" dense class="ma-2">
              {{ errorMessage }}
            </v-alert>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </BaseLayout>
</template>

<script>
import BaseLayout from "@/layouts/BaseLayout.vue";
import { useAuthStore } from '@/plugins/stores/auth';
import Notiflix from 'notiflix';

export default {
  components: {
    BaseLayout,
  },

  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: false,
      errorMessage: '',
      emailRules: [
        v => !!v || 'E-mail is required!',
        v => /.+@.+\..+/.test(v) || 'Please enter a valid email address'
      ],
      passwordRules: [
        v => !!v || 'Password is required!',
      ]
    }
  },

  created() {
    // Eğer kullanıcı giriş yapmışsa dashboard'a yönlendir
    const authStore = useAuthStore()
    if (authStore.isLoggedIn) {
      this.$router.push({ name: 'dashboard' })
    }
  },

  methods: {
    async login() {
      // Validate form using Vuetify's built-in validation
      const isValid = await this.$refs.form.validate();
      if (!isValid) {
        return;
      }

      this.loading = true;
      this.error = false;

      try {
        const authStore = useAuthStore();
        await authStore.loginRequest({
          email: this.email,
          password: this.password
        });

        Notiflix.Notify.success(
          'Login successful!',
          {
            timeout: 3000,
            position: 'right-bottom',
          },
        );

        this.$router.push({ name: 'dashboard' });
      } catch (error) {
        this.error = true;
        this.errorMessage = error.response?.data?.detail || 'Login failed. Please check your credentials.';
        
        Notiflix.Notify.failure(
          this.errorMessage,
          {
            timeout: 5000,
            position: 'right-bottom',
          },
        );
        
        console.error('Login error:', error);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 50vh;
}
</style>