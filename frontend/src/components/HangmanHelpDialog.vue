<template>
  <Dialog v-model:visible="showDialog" modal header="Game Rules">
    <ul>
      <li>Guess the word by suggesting letters.</li>
      <li>Only one character per guess.</li>
      <li>If you guess the word before running out of tries, you win!</li>
      <li>You can guess incorrectly 6 times before losing.</li>
    </ul>
  </Dialog>
</template>

<script setup lang="ts">
const showDialog = defineModel<boolean>();
</script>
