import { createApp } from "vue";
import { createPinia } from "pinia";
import { createI18n } from "vue-i18n";
import PrimeVue from "primevue/config";
import router from "./router";

import App from "./App.vue";
import { customTheme } from "./style/theme";
import "@/style.css";
import "primeicons/primeicons.css";

// Import language messages
import en from "@/languages/en.json";
import de from "@/languages/de.json";

const pinia = createPinia();
const app = createApp(App);

// Get stored language from localStorage
const storedLanguage = localStorage.getItem("language") || "en";

// Create i18n instance with stored language
const i18n = createI18n({
  legacy: false,
  locale: storedLanguage,
  fallbackLocale: "en",
  messages: {
    en,
    de,
  },
});

app.use(PrimeVue, {
  theme: {
    preset: customTheme,
    options: {
      darkModeSelector: ".dark-mode",
    },
  },
});
app.use(pinia);
app.use(router);
app.use(i18n);
app.mount("#app");
