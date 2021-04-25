import Vue from 'vue';
import {VuePlausible} from 'vue-plausible';

Vue.use(VuePlausible, {
  domain: 'check-redirects.com',
  trackLocalhost: true,
});

Vue.$plausible.enableAutoPageviews();
