<template>
  <div>
    <!-- checken ob border in :root oder in App.vue + Reihenfolge fixen-->
    <Navbar>
      <RouterView />
    </Navbar>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
import Navbar from "./components/Navbar.vue";
</script>

<style scoped></style>
