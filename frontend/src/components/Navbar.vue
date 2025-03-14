<template>
  <div id="layout" class="flex-column align-items-center">
    <div id="topBanner" class="flex p-0 m-0 top-0 left-0">
      <div
        class="flex flex-row align-items-center justify-content-between flex-grow-1"
      >
        <div class="flex-initial m-4">
          <img src="../style/buttman.webp" alt="logo" loading="lazy" />
        </div>
        <div class="flex-grow-1">
          <InputText
            type="text"
            v-model="search"
            placeholder="Search"
            class="w-full"
          />
          <!-- w-full extends element to full screen width -->
        </div>
        <div class="flex-initial m-4">
          <Button
            type="button"
            icon="pi pi-ellipsis-v"
            @click="toggle"
            aria-haspopup="true"
            aria-controls="overlay_menu"
            aria-label="Menu"
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
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 100;
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
  box-shadow: 0 0 10px 2px var(--p-zinc-400);
}
</style>
