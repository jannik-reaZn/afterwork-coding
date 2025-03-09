<template>
  <div>
    <Navbar>
      <RouterView />
    </Navbar>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import Navbar from "@/components/Navbar.vue";
</script>

<style scoped></style>
