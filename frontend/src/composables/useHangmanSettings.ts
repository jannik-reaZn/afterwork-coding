import { computed } from "vue";
import { useHangmanStore } from "@/store/hangman";
import capitalizeFirstLetter from "@/utils/utils";

export function useHangmanSettings() {
  const store = useHangmanStore();

  // Data transformation
  const triesOptions = computed(() => {
    return (
      store.settings?.tries?.map((triesCount: number) => ({
        name: triesCount,
        tries: triesCount,
      })) || []
    );
  });

  const languageOptions = computed(() => {
    return (
      store.settings?.languages?.map((language: string) => ({
        name: capitalizeFirstLetter(language),
        language: capitalizeFirstLetter(language),
      })) || []
    );
  });

  // Default values
  const defaultTry = computed(() => store.settings?.tries?.[0]);
  const defaultLanguage = computed(() => {
    return store.settings?.languages?.[0]
      ? capitalizeFirstLetter(store.settings.languages[0])
      : undefined;
  });

  // Data loading
  async function loadSettings() {
    await store.getSettings();
  }

  return {
    triesOptions,
    languageOptions,
    defaultTry,
    defaultLanguage,
    loadSettings,
  };
}
