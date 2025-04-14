<template>
  <BaseLayout>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h5">
              My Shortened URLs
            </v-card-title>

            <v-card-text>
              <v-data-table
                :headers="headers"
                :items="urls"
                :loading="loading"
                :items-per-page="10"
                class="elevation-1"
              >
                <template v-slot:item.original_url="{ item }">
                  <a :href="item.original_url" target="_blank" class="text-decoration-none">
                    {{ truncateUrl(item.original_url) }}
                  </a>
                </template>

                <template v-slot:item.short_url="{ item }">
                  <div class="d-flex align-center">
                    <a :href="item.short_url" target="_blank" class="text-decoration-none">
                      {{ item.short_url }}
                    </a>
                    <v-btn
                      icon
                      small
                      class="ml-2"
                      @click="copyToClipboard(item.short_url)"
                    >
                      <v-icon small>mdi-content-copy</v-icon>
                    </v-btn>
                  </div>
                </template>

                <template v-slot:item.created_at="{ item }">
                  {{ formatDate(item.created_at) }}
                </template>

                <template v-slot:item.actions="{ item }">
                  <v-btn
                    icon
                    small
                    color="error"
                    @click="deleteUrl(item.id)"
                  >
                    <v-icon small>mdi-delete</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-snackbar
        v-model="snackbar"
        :timeout="2000"
        color="success"
      >
        {{ snackbarText }}
      </v-snackbar>
    </v-container>
  </BaseLayout>
</template>

<script>
import BaseLayout from "@/layouts/BaseLayout.vue";
import ShortenService from "@/services/shorten-service.js";
import { useAuthStore } from '@/plugins/stores/auth';
import Notiflix from 'notiflix';

export default {
  components: {
    BaseLayout,
  },
  data() {
    return {
      urls: [],
      loading: false,
      snackbar: false,
      snackbarText: '',
      headers: [
        { text: 'Original URL', value: 'original_url' },
        { text: 'Short URL', value: 'short_url' },
        { text: 'Created At', value: 'created_at' },
        { text: 'Visits', value: 'visits' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
    }
  },
  created() {
    this.fetchUrls();
  },
  methods: {
    async fetchUrls() {
      this.loading = true;
      try {
        const response = await ShortenService.getUserUrls();
        this.urls = response.data.results;
      } catch (error) {
        console.error('Failed to fetch URLs:', error);
      } finally {
        this.loading = false;
      }
    },
    async deleteUrl(id) {
      Notiflix.Confirm.show(
    'URL Delete Confirmation',
    'Are you sure you want to delete this URL?',
    'Yes',
    'No',
    async () => {
      try {
        await ShortenService.deleteUrl(id);
        this.urls = this.urls.filter(url => url.id !== id);
        this.showSnackbar('URL successfully deleted');
      } catch (error) {
        console.error('URL could not be deleted:', error);
        this.showSnackbar('URL could not be deleted', 'error');
      }
    },
    () => {
      this.showSnackbar('Delete operation cancelled');
    },
    {}
  );
},

    copyToClipboard(text) {
      navigator.clipboard.writeText(text)
        .then(() => {
          this.showSnackbar('URL copied to clipboard');
        })
        .catch(err => {
          console.error('Copy failed:', err);
          this.showSnackbar('Failed to copy URL', 'error');
        });
    },
    truncateUrl(url) {
      if (url.length > 50) {
        return url.substring(0, 50) + '...';
      }
      return url;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    },
    showSnackbar(text, type = 'success') {
      this.snackbarText = text;
      this.snackbar = true;
    }
  }
}
</script>

<style scoped>
.v-data-table {
  width: 100%;
}
</style>