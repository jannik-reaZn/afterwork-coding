<template>
  <Card class="custom-card">
    <template #title>
      <h2 class="p-card-title text-center">
        <slot name="title">Hangman</slot>
      </h2>
    </template>
    <template #content>
      <p class="p-card-content text-gray-600 text-center">
        <slot name="content">
          Try to guess the word before you run out of attempts!
        </slot>
      </p>
    </template>
    <template #footer v-if="props.showButton">
      <div class="p-card-footer">
        <Button
          class="px-4 py-2 text-white rounded-lg shadow-md hover:bg-blue-600 transition duration-200"
          @click="openGame"
          >Open Game
        </Button>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";

const props = defineProps<{
  navigateTo?: string;
  showButton?: boolean;
}>();

const router = useRouter();
const openGame = () => {
  if (!props.navigateTo) return;
  router.push(props.navigateTo);
};
</script>

<style scoped>
.custom-card {
  --p-card-background: white;
  --p-card-border-radius: 1rem;
  --p-card-color: black;
  border: 2px solid lightgrey;
}

.p-card-title {
  --p-card-title-font-size: 1.5rem;
  --p-card-title-font-weight: bold;
}

.p-card-footer {
  display: flex;
  justify-content: center;
}
</style>
