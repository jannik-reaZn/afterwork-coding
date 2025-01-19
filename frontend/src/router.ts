import { createWebHistory, createRouter } from "vue-router";

import Home from "./view/Home.vue";
import Example from "./view/Example.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/example", component: Example },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
