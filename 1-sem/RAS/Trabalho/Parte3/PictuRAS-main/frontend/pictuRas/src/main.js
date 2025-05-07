import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

import VueColor from '@ckpack/vue-color';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPlay, faPause } from '@fortawesome/free-solid-svg-icons';

library.add(faPlay, faPause);

const pinia = createPinia();

const app = createApp(App);
app.use(pinia);
app.use(router);
app.use(VueColor);
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');
