import { defineStore } from "pinia";
import { ref, watchEffect } from "vue";
import { useI18n } from "vue-i18n";

export const useLanguageStore = defineStore("language", () => {
  const i18n = useI18n();
  // State
  const language = ref(localStorage.getItem("language") || "en");

  // Actions
  function setLanguage(lang: string) {
    language.value = lang;
    localStorage.setItem("language", lang);
    // Update i18n locale when language changes
    i18n.locale.value = lang;
  }

  // Watch for changes and update DOM/localStorage
  watchEffect(() => {
    const html = document.documentElement;
    html.setAttribute("language", language.value);
  });

  return { language, setLanguage };
});
