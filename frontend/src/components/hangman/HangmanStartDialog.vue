<template>
  <Dialog
    v-model:visible="showHangmanModal"
    modal
    header="Hangman Game"
    class="w-1/3"
    :closable="false"
    :closeOnEscape="false"
    :dismissableMask="false"
    :draggable="false"
  >
    <span class="text-surface-500 mb-4 block">Select game options.</span>
    <div class="grid grid-cols-2 gap-4">
      <label for="tries" class="text-surface-500">Number of tries</label>
      <Select
        v-model="selectedTry"
        :options="tries"
        optionLabel="name"
        optionValue="tries"
        size="small"
      />
    </div>

    <div class="grid grid-cols-2 gap-4">
      <label for="language" class="text-surface-500">Language</label>
      <Select
        v-model="selectedLanguage"
        :options="languages"
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
    ></Button>
  </Dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";

// Store
import { useHangmanStore } from "@/store/hangman";
const store = useHangmanStore();

const showHangmanModal = defineModel<boolean>({ required: true });

const NUMBER_OF_TRIES = 6;

const selectedTry = ref<number>(NUMBER_OF_TRIES);

// TODO This should be fetched from the backend
const tries = ref([
  { name: NUMBER_OF_TRIES, tries: 6 },
  { name: 7, tries: 7 },
  { name: 8, tries: 8 },
  { name: 9, tries: 9 },
]);

const selectedLanguage = ref<string>("American");
const languages = ref([
  { name: "American", language: "American" },
  { name: "German", language: "German" },
]);

function startGame() {
  showHangmanModal.value = false;
  store.startGame(selectedTry.value, selectedLanguage.value);
}
</script>

<style scoped></style>
