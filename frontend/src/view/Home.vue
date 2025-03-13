<template>
  <Card>
    <template #title>Hangman</template>
    <template #content>
      <p class="m-0">Description for hangman game.</p>
    </template>
    <template #footer>
      <div class="flex gap-4 mt-1">
        <RouterLink to="/hangman">Open</RouterLink>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts"></script>

<style scoped></style>
