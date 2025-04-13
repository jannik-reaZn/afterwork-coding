<template>
  <header class="bg-footer sticky top-0 z-20 shadow-lg">
    <nav class="py-4 text-white">
      <div class="flex items-center justify-between gap-1 px-2">
        <img
          src="../style/buttman.webp"
          alt="logo"
          loading="lazy"
          @click="navigateToHome"
          class="cursor-pointer"
        />
        <InputText
          type="text"
          class="w-full"
          v-model="search"
          placeholder="Search"
        />
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
    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

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

const navigateToHome = () => {
  router.push("/");
};
</script>

<style scoped>
img {
  width: 8vh;
  min-width: 50px;
  height: auto;
  border: 1px solid transparent;
  border-radius: 9px;
  transition: box-shadow 0.3s ease-in-out;
}
</style>
