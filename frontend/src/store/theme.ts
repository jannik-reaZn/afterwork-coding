import { defineStore } from "pinia";
import { ref, watchEffect } from "vue";

export const useThemeStore = defineStore("theme", () => {
  // State
  const isDarkMode = ref(localStorage.getItem(".dark-mode") === "true");

  // Actions
  function toggleDarkMode() {
    isDarkMode.value = !isDarkMode.value;
  }

  // Watch for changes and update DOM/localStorage
  watchEffect(() => {
    const html = document.documentElement;
    if (isDarkMode.value) {
      html.classList.add("dark-mode");
    } else {
      html.classList.remove("dark-mode");
    }
    localStorage.setItem(".dark-mode", isDarkMode.value.toString());
  });

  return { isDarkMode, toggleDarkMode };
});
