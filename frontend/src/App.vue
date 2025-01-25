<template>
  <LogIn />
  <div>
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import HelloWorld from "@/components/HelloWorld.vue";
import LogIn from "@/components/LogIn.vue";
import { RouterView } from "vue-router";
</script>

<style scoped></style>
