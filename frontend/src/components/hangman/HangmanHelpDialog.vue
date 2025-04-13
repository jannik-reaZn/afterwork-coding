<template>
  <Dialog
    v-model:visible="showDialog"
    modal
    header="Game Rules"
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
const showDialog = defineModel<boolean>();

const rules = [
  "Guess the word by suggesting letters.",
  "Only one character per guess.",
  "If you guess the word before running out of tries, you win!",
];
</script>
