<template>
  <v-app-bar app class="brown darken-4">
    <v-app-bar-nav-icon
      v-if="isLoggedIn"
      @click="toggleDrawer"
    ></v-app-bar-nav-icon>
    <router-link to="/" class="text-white text-decoration-none">
      <v-app-bar-title class="pl-5">URL Shortener</v-app-bar-title>
    </router-link>

    <v-spacer></v-spacer>

    <v-avatar
      v-if="isLoggedIn"
      size="36"
      class="mr-2"
      image="https://uhcspecialties.com/wp-content/uploads/2023/09/Daniel-D.-Sutphin-MD-BlueBack-scaled.jpg"
    ></v-avatar>

    <v-btn
      v-if="!isLoggedIn"
      text
      :to="{ name: 'login' }"
      component="RouterLink"
      >Login</v-btn
    >
    <v-btn
      v-if="!isLoggedIn"
      outlined
      :to="{ name: 'register' }"
      component="RouterLink"
    >
      Register
    </v-btn>

    <v-menu v-if="isLoggedIn" offset-y>
      <template v-slot:activator="{ props }">
        <v-btn variant="text" v-bind="props">
          {{ userData.name }} {{ userData.surname }}
          <v-icon>keyboard_arrow_down</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item>
          <v-btn
            class="d-flex align-center"
            variant="text"
            block
            @click="logout"
          >
            <v-icon class="mr-5" size="20">mdi-logout</v-icon>
            Logout
          </v-btn>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
import LogoutMixin from "@/mixins/LogoutMixin";
import { useAuthStore } from "@/plugins/stores/auth";
import { storeToRefs } from "pinia";

export default {
  mixins: [LogoutMixin],
  inject: ["state"],
  data() {
    return {
      userData: {
        name: "",
        surname: "",
      },
    };
  },
  created() {
    this.authStore = useAuthStore();
    if (this.authStore.isLoggedIn) {
      this.fetchUserData();
    }
  },
  methods: {
    toggleDrawer() {
      this.state.drawer = !this.state.drawer;
    },
    async fetchUserData() {
      try {
        await this.authStore.getUserData();
        const { userData } = storeToRefs(this.authStore);
        this.userData = userData.value;
      } catch (error) {
        console.error("Kullanıcı bilgileri alınamadı:", error);
      }
    },
  },
};
</script>
