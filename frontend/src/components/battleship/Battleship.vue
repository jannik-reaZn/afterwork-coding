<template>
  <div
    ref="el"
    :style="style"
    :class="['flex', props.orientation === Orientation.Vertical && 'flex-col']"
    style="position: absolute; cursor: move"
  >
    <div
      class="size-6 border-1"
      v-for="(_, index) in props.size"
      :key="index"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue";
import { useDraggable } from "@vueuse/core";
import { ref } from "vue";
import { Orientation } from "@/models/battleship/battleshipOrientation";

const el = ref<HTMLElement | null>(null);

const { style } = useDraggable(el, {
  initialValue: { x: 200, y: 200 },
});

const props = defineProps({
  size: {
    type: Number,
    default: 3,
  },
  orientation: {
    type: String as PropType<Orientation>,
    default: Orientation.Horizontal,
  },
});
</script>

<style scoped></style>
