import vuetify from './vuetify/vuetify';
import router from './router/index';
import pinia from './stores/index'; 

export function registerPlugins(app) {
  app.use(pinia);
  app.use(vuetify);
  app.use(router);
}
