<template>
  <header
    class="bg-footer sticky top-0 z-20 shadow-lg"
    :class="{
      'shadow-[#18181B]': themeStore.isDarkMode,
      'shadow-gray-300': !themeStore.isDarkMode,
    }"
  >
    <nav class="py-4">
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
          :placeholder="t('navbar.search.placeholder')"
        />
        <Button
          :icon="themeStore.isDarkMode ? 'pi pi-moon' : 'pi pi-sun'"
          @click="themeStore.toggleDarkMode"
          class="p-button-outlined"
          aria-label="Dark Mode"
          aria-haspopup="true"
          aria-controls="dark_mode"
        />
        <Button
          type="button"
          icon="pi pi-cog"
          @click="toggle"
          aria-haspopup="true"
          aria-controls="overlay_menu"
          aria-label="Menu"
        />
        <Menu ref="menu" id="overlay_menu" :model="items" :popup="true" />
      </div>
    </nav>
  </header>
  <SettingsDialog v-model="showSettingsDialog" />
</template>

<script setup lang="ts">
import { ref } from "vue";
import SettingsDialog from "@/components/settings/SettingsDialog.vue";

// Theme
import { useThemeStore } from "@/store/theme";
const themeStore = useThemeStore();

// Internationalization
import { useI18n } from "vue-i18n";
const { t } = useI18n();

// Menu
const menu = ref();
const showSettingsDialog = ref(false);
const items = ref([
  {
    items: [
      {
        label: t("navbar.settings.title"),
        icon: "pi pi-cog",
        command: () => (showSettingsDialog.value = true),
      },
      {
        label: t("navbar.settings.logout.title"),
        icon: "pi pi-sign-out",
      },
    ],
  },
]);

const toggle = (event: Event) => {
  menu.value.toggle(event);
};

const search = ref(null);

// Navigation
import { useRouter } from "vue-router";
const router = useRouter();
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
