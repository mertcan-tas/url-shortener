<template>
  <BaseLayout>


    
    <v-container fluid class="pa-4" style="margin-top: 15vh;">
      <v-row justify="center" align="center">
        <v-col cols="12" sm="10" md="8" lg="6">
          <v-card elevation="10" class="pa-6 text-center">
            <v-card-title class="text-h4 justify-center mb-4">
              Shorten Your URL
            </v-card-title>
            
            <v-card-subtitle class="mb-4">
              Quickly shorten your long links and make sharing easier
            </v-card-subtitle>

            <v-form @submit.prevent="shortenUrl">
              <v-text-field
                v-model="originalUrl"
                label="Enter your URL"
                placeholder="https://example.com/very-long-url-address"
                outlined
                :rules="[rules.required, rules.url]"
                prepend-inner-icon="mdi-link"
                clearable
              ></v-text-field>

              <!-- Error Alert -->
              <v-alert v-if="errorMessage" type="error" class="mb-4">
                {{ errorMessage }}
              </v-alert>

              <v-btn
              class="mt-3"
                color="primary"
                x-large
                block
                depressed
                type="submit"
                :loading="loading"
                :disabled="!originalUrl"
              >
                Shorten URL
              </v-btn>
            </v-form>

            <v-expand-transition>
              <div v-if="shortenedUrl">
                <v-divider class="my-4"></v-divider>
                <v-card-text>
                  <v-alert type="success" class="mb-4">
                    Your URL has been successfully shortened!
                  </v-alert>

                  <div class="d-flex align-center">
                    <v-text-field
                      v-model="shortenedUrl"
                      outlined
                      readonly
                      class="flex-grow-1 mr-2"
                    ></v-text-field>
                    <v-btn
                    class="mb-4"
                      icon
                      color="primary"
                      @click="copyToClipboard"
                      title="Copy to clipboard"
                    >
                      <v-icon>mdi-content-copy</v-icon>
                    </v-btn>
                  </div>

                  <v-snackbar
                    v-model="snackbar"
                    :timeout="2000"
                    color="success"
                  >
                    Short URL copied to clipboard!
                  </v-snackbar>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>

          <v-card class="mt-6 pa-4" elevation="4">
            <v-row justify="center" align="center">
              <v-col cols="4" class="text-center">
                <v-icon size="36" color="primary">mdi-flash</v-icon>
                <div class="text-h6 mt-2">Fast</div>
                <div class="text-caption">Shorten in seconds</div>
              </v-col>
              <v-col cols="4" class="text-center">
                <v-icon size="36" color="primary">mdi-chart-line</v-icon>
                <div class="text-h6 mt-2">Statistics</div>
                <div class="text-caption">Click analytics</div>
              </v-col>
              <v-col cols="4" class="text-center">
                <v-icon size="36" color="primary">mdi-shield-check</v-icon>
                <div class="text-h6 mt-2">Secure</div>
                <div class="text-caption">Secure link management</div>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </BaseLayout>
</template>

<script>
import BaseLayout from "@/layouts/BaseLayout.vue";
import ShortenService from "@/services/shorten-service.js";
import { useAuthStore } from '@/plugins/stores/auth';

export default {
  components: {
    BaseLayout,
  },
  data: () => ({
    originalUrl: '',
    shortenedUrl: '',
    loading: false,
    snackbar: false,
    errorMessage: null,
    rules: {
      required: value => !!value || 'This field is required',
      url: value => {
        const pattern = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/;
        return pattern.test(value) || 'Please enter a valid URL';
      }
    },
  }),

  methods: {
    async shortenUrl() {
      if (!this.originalUrl) return;

      this.loading = true;
      this.errorMessage = null;
      
      try {
        const authStore = useAuthStore();
        
        // URL'yi kısalt
        const response = await ShortenService.createShortenUrl({
          original_url: this.originalUrl
        });
        
        if (response.data && response.data.short_url) {
          this.shortenedUrl = response.data.short_url;
          this.originalUrl = "";
        } else {
          throw new Error('Invalid response format');
        }
      } catch (error) {
        console.error('Shortening failed:', error);
        if (error.response?.status === 401) {
          this.errorMessage = 'Please login to shorten URLs';
        } else {
          this.errorMessage = error.response?.data?.message || 'Failed to shorten URL. Please try again.';
        }
      } finally {
        this.loading = false;
      }
    },

    copyToClipboard() {
      navigator.clipboard.writeText(this.shortenedUrl)
        .then(() => {
          this.snackbar = true;
        })
        .catch(err => {
          console.error('Copy failed:', err);
          this.errorMessage = 'Failed to copy to clipboard';
        });
    }
  }
};
</script>