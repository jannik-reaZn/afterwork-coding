<template>
  <Dialog
    v-model:visible="showDialog"
    modal
    :header="$t('hangman.rules.title')"
    class="xxl:w-1/4 w-5/6 sm:w-1/2 xl:w-1/3"
    :dismissableMask="true"
    :draggable="false"
  >
    <ul class="list-disc pl-5">
      <li v-for="(rule, idx) in rules" :key="idx">{{ rule }}</li>
    </ul>
  </Dialog>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
const { tm } = useI18n();
const rules = tm("hangman.rules.items");

const showDialog = defineModel<boolean>();
</script>
