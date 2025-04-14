<template>
  <Dialog
    v-model:visible="showHangmanModal"
    modal
    header="Hangman Game"
    class="xxl:w-1/4 w-5/6 sm:w-1/2 xl:w-1/3"
    :closable="false"
    :closeOnEscape="false"
    :dismissableMask="false"
    :draggable="false"
  >
    <div class="grid grid-cols-2 gap-4">
      <label for="tries">Number of tries</label>
      <Select
        v-model="selectedTry"
        :options="triesOptions"
        optionLabel="name"
        optionValue="tries"
        size="small"
      />
    </div>

    <div class="grid grid-cols-2 gap-4">
      <label for="language">Language</label>
      <Select
        v-model="selectedLanguage"
        :options="languageOptions"
        optionLabel="name"
        optionValue="language"
        size="small"
      />
    </div>

    <Button
      type="submit"
      label="Start Game"
      class="mt-2 w-full"
      size="small"
      @click="startGame"
    />
  </Dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useHangmanSettings } from "@/composables/useHangmanSettings";
import { DEFAULT_NUMBER_OF_TRIES, DEFAULT_LANGUAGE } from "@/constants/hangman";
import { useHangmanStore } from "@/store/hangman";

// Store
const store = useHangmanStore();

// Props/Model
const showHangmanModal = defineModel<boolean>({ required: true });

// Composables
const {
  triesOptions,
  languageOptions,
  defaultTry,
  defaultLanguage,
  loadSettings,
} = useHangmanSettings();

// State
const selectedTry = ref<number>();
const selectedLanguage = ref<string>();

// Lifecycle
onMounted(async () => {
  await loadSettings();
  selectedTry.value = defaultTry.value;
  selectedLanguage.value = defaultLanguage.value;
});

// Methods
function startGame() {
  showHangmanModal.value = false;
  const tries = selectedTry.value ?? DEFAULT_NUMBER_OF_TRIES;
  const language = selectedLanguage.value ?? DEFAULT_LANGUAGE;
  store.startGame(tries, language);
}
</script>
