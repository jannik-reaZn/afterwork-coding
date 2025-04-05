import { defineConfig } from "vite";
import VueRouter from "unplugin-vue-router/vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
// auto import of PrimeVue components
import Components from "unplugin-vue-components/vite";
import { PrimeVueResolver } from "@primevue/auto-import-resolver";

export default defineConfig({
  plugins: [
    VueRouter(),
    vue(),
    tailwindcss(),
    Components({
      resolvers: [PrimeVueResolver()],
    }),
  ],
  server: {
    watch: {
      usePolling: true,
    },
  },
  resolve: {
    alias: {
      "@": "/src",
    },
  },
});
