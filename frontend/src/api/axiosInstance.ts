import axios from "axios";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_AXIOS_BACKENDURL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
