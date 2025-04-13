<template>
  <div class="flex min-h-screen flex-col">
    <Navbar />
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import Navbar from "@/components/Navbar.vue";
</script>

<style scoped></style>
