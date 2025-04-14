<template>
<v-navigation-drawer v-model="state.drawer">
    <v-list>
      <v-list-item
        v-for="item in mainMenu"
        :key="item.title"
        :to="item.to"
        link
        router
        class="py-2 px-3"
      >
        <v-list-item-title class="d-flex align-center">
          <v-icon class="mr-2" size="20">{{ item.icon }}</v-icon>
          {{ item.title }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  inject: ['state'],
  data() {
    return {
      mainMenu: [
        { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/dashboard' },
        { title: 'Shorten Url', icon: 'mdi-link-variant-plus', to: '/shorten-url' },
        { title: 'My Urls', icon: 'mdi-playlist-check', to: '/my-urls' },
        
      ],
    }
  },
  
}
</script>