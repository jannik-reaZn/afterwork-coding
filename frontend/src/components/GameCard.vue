<template>
  <Card class="custom-card">
    <template #title>
      <h2 class="p-card-title text-center">
        <slot name="title"></slot>
      </h2>
    </template>
    <template #content>
      <p class="p-card-content text-center">
        <slot name="content"></slot>
      </p>
    </template>
    <template #footer v-if="props.showButton">
      <div class="p-card-footer">
        <Button class="rounded-lg px-4 py-2" @click="openGame">
          {{ $t("card.button.title") }}
        </Button>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";

const props = defineProps<{
  navigateTo?: string | null;
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
  --p-card-border-radius: 1rem;
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
