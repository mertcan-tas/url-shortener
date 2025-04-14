<template>
  
 <BaseLayout>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Register</v-toolbar-title>
          </v-toolbar>
          
          <v-card-text>
            <v-form @submit.prevent="register">
              <v-text-field
                v-model="email"
                label="Email"
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
              
              <v-text-field
                v-model="password2"
                label="Confirm Password"
                class="mb-5 mt-4"
                prepend-icon="mdi-lock-check"
                type="password"
                required
                :rules="confirmPasswordRules"
              ></v-text-field>
              
              <v-text-field
                v-model="name"
                label="Name"
                class="mb-5 mt-4"
                prepend-icon="mdi-account"
                required
                :rules="nameRules"
              ></v-text-field>
              
              <v-text-field
                v-model="surname"
                label="Surname"
                class="mb-5 mt-4"
                prepend-icon="mdi-account"
                required
                :rules="surnameRules"
              ></v-text-field>

              <v-btn 
                type="submit" 
                color="primary" 
                block
                :loading="loading"
              >
                Register
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
   </BaseLayout>

  
</template>

<script>
import { useAuthStore } from '@/plugins/stores/auth'
import Notiflix from 'notiflix';
import BaseLayout from "@/layouts/BaseLayout.vue";

export default {
  components: {
    BaseLayout,
  },
  data() {
    return {
      email: '',
      password: '',
      password2: '',
      name: '',
      surname: '',
      loading: false,
      emailRules: [
        v => !!v || 'Email is required!',
        v => /.+@.+\..+/.test(v) || 'Enter a valid email address'
      ],
      passwordRules: [
        v => !!v || 'Password is required!',
        v => v.length >= 6 || 'Password must be at least 6 characters'
      ],
      confirmPasswordRules: [
        v => !!v || 'Confirm Password is required!',
        v => v === this.password || 'Passwords do not match'
      ],
      nameRules: [
        v => !!v || 'Name is required!'
      ],
      surnameRules: [
        v => !!v || 'Surname is required!'
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
    async register() {
      if (!this.validateForm()) return
      
      this.loading = true
      
      try {
        const authStore = useAuthStore()
        await authStore.registerRequest({
          email: this.email,
          password: this.password,
          password2: this.password2,
          name: this.name,
          surname: this.surname,
        });
        
        Notiflix.Notify.success(
          'Registration successful!',
          {
            timeout: 5000,
            position: 'right-bottom',
          },
        );

        // Kayıt başarılı olduktan sonra login sayfasına yönlendir
        this.$router.push({ name: 'login' })
        
      } catch (error) {
        Notiflix.Notify.failure(
          'Registration failed. Please check your information.',
          {
            timeout: 5000,
            position: 'right-bottom',
          },
        );
        console.error('Registration error:', error);
      } finally {
        this.loading = false
      }
    },
    validateForm() {
      return this.emailRules.every(rule => rule(this.email) === true) &&
             this.passwordRules.every(rule => rule(this.password) === true) &&
             this.confirmPasswordRules.every(rule => rule(this.password2) === true) &&
             this.nameRules.every(rule => rule(this.name) === true) &&
             this.surnameRules.every(rule => rule(this.surname) === true)
    }
  }
}
</script>

