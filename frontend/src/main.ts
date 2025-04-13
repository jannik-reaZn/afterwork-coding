import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";

// PrimeVue
import PrimeVue from "primevue/config";
import "primeicons/primeicons.css";

// PrimeVue Components
import ToastService from "primevue/toastservice";

import { customTheme } from "./style/theme";
import "@/style.css";

const pinia = createPinia();
const app = createApp(App);

app.use(router);
app.use(pinia);
app.use(PrimeVue, {
  theme: {
    preset: customTheme,
    options: {
      darkModeSelector: false,
    },
  },
});
app.use(ToastService);
app.mount("#app");
