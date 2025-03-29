<template>
  <Dialog v-model:visible="showDialog" modal header="Game Rules">
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
  "You can guess incorrectly 6 times before losing.",
];
</script>
