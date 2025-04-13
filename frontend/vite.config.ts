import { defineConfig, loadEnv } from "vite";
import VueRouter from "unplugin-vue-router/vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
// auto import of PrimeVue components
import Components from "unplugin-vue-components/vite";
import { PrimeVueResolver } from "@primevue/auto-import-resolver";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [
      VueRouter(),
      vue(),
      tailwindcss(),
      Components({
        resolvers: [PrimeVueResolver()],
      }),
    ],
    server: {
      port: parseInt(env.VITE_PORT, 10) || 3000,
      watch: {
        usePolling: true,
      },
    },
    resolve: {
      alias: {
        "@": "/src",
      },
    },
  };
});
