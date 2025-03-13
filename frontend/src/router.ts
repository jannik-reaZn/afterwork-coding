import { createWebHistory, createRouter } from "vue-router";

import Home from "@/view/Home.vue";
import Example from "@/view/Example.vue";
import Hangman from "@/view/Hangman.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/example", component: Example },
  { path: "/hangman", component: Hangman }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
