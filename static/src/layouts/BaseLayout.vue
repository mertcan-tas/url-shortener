<template>
  <div id="app">
    <v-app>
      <Appbar />
      <NavigationDrawer v-if="isLoggedIn"></NavigationDrawer>
      <v-main>
        <slot></slot>
      </v-main>
      <Footer />
    </v-app>
  </div>
</template>

<script>
import Appbar from "@/layouts/Appbar.vue";
import NavigationDrawer from "@/layouts/NavigationDrawer.vue";
import Footer from "@/layouts/Footer.vue";
import LogoutMixin from "@/mixins/LogoutMixin";

export default {
  mixins: [LogoutMixin],
  components: {
    Appbar,
    NavigationDrawer, 
    Footer,
  },
  data() {
    return {
      state: { drawer: true } 
    };
  },
  provide() {
    return {
      state: this.state 
    };
  }
};
</script>