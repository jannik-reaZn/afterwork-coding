<template>
  <Dialog
    v-model:visible="showHangmanModal"
    modal
    :header="$t('hangman.title')"
    class="xxl:w-1/4 w-5/6 sm:w-1/2 xl:w-1/3"
    :closable="false"
    :closeOnEscape="false"
    :dismissableMask="false"
    :draggable="false"
  >
    <div class="grid grid-cols-2 gap-4">
      <label for="tries">{{ $t("hangman.numberOfTries") }}</label>
      <Select
        v-model="selectedTry"
        :options="triesOptions"
        optionLabel="name"
        optionValue="tries"
        size="small"
      />
    </div>

    <div class="grid grid-cols-2 gap-4">
      <label for="language">{{ $t("hangman.language") }}</label>
      <Select
        v-model="selectedLanguage"
        :options="languageOptions"
        optionLabel="name"
        optionValue="language"
        size="small"
      />
    </div>

    <div class="grid grid-cols-2 gap-4">
      <label for="mode">{{ $t("hangman.mode") }}</label>
      <Select
        v-model="selectedMode"
        :options="modeOptions"
        optionLabel="name"
        optionValue="mode"
        size="small"
      />
    </div>
    <Button
      type="submit"
      :label="$t('hangman.startGame')"
      class="mt-2 w-full"
      size="small"
      @click="startGame"
    />
  </Dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useHangmanSettings } from "@/composables/useHangmanSettings";
import {
  DEFAULT_NUMBER_OF_TRIES,
  DEFAULT_LANGUAGE,
  DEFAULT_MODE,
} from "@/constants/hangman";

// Store
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();

// Props/Model
const showHangmanModal = defineModel<boolean>({ required: true });

// Composables
const {
  triesOptions,
  languageOptions,
  modeOptions,
  defaultTry,
  defaultLanguage,
  defaultMode,
  loadSettings,
} = useHangmanSettings();

// State
const selectedTry = ref<number>();
const selectedLanguage = ref<string>();
const selectedMode = ref<string>();

// Lifecycle
onMounted(async () => {
  await loadSettings();
  selectedTry.value = defaultTry.value;
  selectedLanguage.value = defaultLanguage.value;
  selectedMode.value = defaultMode.value;
});

// Methods
function startGame() {
  showHangmanModal.value = false;
  const tries = selectedTry.value ?? DEFAULT_NUMBER_OF_TRIES;
  const language = selectedLanguage.value ?? DEFAULT_LANGUAGE;
  const mode = selectedMode.value ?? DEFAULT_MODE;
  store.startGame(tries, language, mode);
}
</script>
