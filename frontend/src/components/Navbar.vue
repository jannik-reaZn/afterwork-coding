<!-- Home vue -> Komponenten aufsplitten -> App.vue -->

<template>
  <!-- layout -->
  <div id="layout" class="flex-column align-items-center">
    <!-- Top Banner -->
    <div id="topBanner" class="flex p-0 m-0 top-0 left-0">
      <div
        class="flex flex-row align-items-center justify-content-between flex-grow-1"
      >
        <div class="flex-initial m-4">
          <img src="../style/buttman.webp" alt="logo" />
        </div>
        <div class="flex-grow-1">
          <InputText
            type="text"
            v-model="search"
            placeholder="Search"
            class="w-full"
          />
          <!-- w-full nimmt die volle Breite des Parents ein -->
        </div>
        <div class="flex-initial m-4">
          <Button
            type="button"
            icon="pi pi-ellipsis-v"
            @click="toggle"
            aria-haspopup="true"
            aria-controls="overlay_menu"
          />
          <Menu ref="menu" id="overlay_menu" :model="items" :popup="true" />
        </div>
      </div>
    </div>
    <div id="slot">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const menu = ref();
const items = ref([
  {
    label: "Profile",
    items: [
      {
        label: "Settings",
        icon: "pi pi-cog",
      },
      {
        label: "Logout",
        icon: "pi pi-sign-out",
      },
    ],
  },
]);

const toggle = (event: Event) => {
  menu.value.toggle(event);
};
const search = ref(null);
</script>

<style scoped>
#topBanner {
  background-color: var(--p-surface-300);
  /* height: 5em; */
  /* min-height: 50px; */
  width: 100vw;
}
img {
  width: 8vh;
  min-width: 50px;
  height: auto;
  border: 1px solid transparent;
  border-radius: 9px;
  transition: box-shadow 0.3s ease-in-out;
}
img:hover {
  /* box-shadow: 0 0 5px 0 var(--p-primary-200); */
  box-shadow: 0 0 10px 2px var(--p-zinc-400);
}
</style>
