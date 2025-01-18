import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import axios from "axios";

// axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;

const app = createApp(App);
// axios.defaults.baseURL = `${import.meta.env.VITE_AXIOS_BASEURL}${
//   import.meta.env.VITE_AXIOS_BACKENDURL
// }`;
// axios.defaults.headers = {
//   ...axios.defaults.headers,
//   "Content-Type": "application/json",
// };

app.mount("#app");
