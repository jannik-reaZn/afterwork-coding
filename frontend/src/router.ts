import { createRouter, createWebHistory } from "vue-router";
import { routes } from "vue-router/auto-routes";
import NotFound from "@/pages/NotFound.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [...routes, { path: "/:pathMatch(.*)*", component: NotFound }],
});

export default router;
