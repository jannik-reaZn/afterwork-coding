import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";

import PrimeVue from "primevue/config";
import "primeflex/primeflex.css";
import "primeicons/primeicons.css";

// PrimeVue components
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Menubar from "primevue/menubar";
import Menu from "primevue/menu";
import Toast from "primevue/toast";
import ToastService from "primevue/toastservice";
import Card from 'primevue/card';


import { customTheme } from "./style/theme";
import "./style.css"; //Loaded last, because it overwrites PrimeVues default styles

const pinia = createPinia();
const app = createApp(App);

app.use(router);
app.use(pinia);
app.use(PrimeVue, {
  theme: {
    preset: customTheme,
    options: {
      darkModeSelector: false, // use 'system' alternatively
    },
  },
});
app.component("Menubar", Menubar);
app.component("Button", Button);
app.component("Toast", Toast);
app.component("InputText", InputText);
app.component("Menu", Menu);
app.component("Card", Card);
app.component("InputText", InputText);
app.use(ToastService);
app.mount("#app");
