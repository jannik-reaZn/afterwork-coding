<template>
  <Dialog
    v-model:visible="visible"
    modal
    :header="t('navbar.settings.title')"
    class="xxl:w-1/4 w-5/6 sm:w-1/2 xl:w-1/3"
    :dismissableMask="true"
    :draggable="false"
  >
    <div class="p-fluid">
      <div class="field mb-4">
        <div class="grid grid-cols-2 items-center gap-4">
          <label for="language" class="col-span-1">
            {{ $t("navbar.settings.language.title") }}
          </label>
          <Select
            id="language"
            v-model="selectedLanguage"
            :options="languages"
            optionLabel="name"
            optionValue="code"
            class="col-span-1"
            :placeholder="t('navbar.settings.language.placeholder')"
          />
        </div>
      </div>
    </div>
    <template #footer>
      <div class="flex justify-end gap-2">
        <Button
          :label="t('navbar.settings.language.cancel')"
          icon="pi pi-times"
          @click="closeDialog"
          class="p-button-text"
        />
        <Button
          :label="t('navbar.settings.language.save')"
          icon="pi pi-check"
          @click="saveSettings"
          autofocus
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

// Store
import { useLanguageStore } from "@/store/language";
const languageStore = useLanguageStore();

// Internationalization
import { useI18n } from "vue-i18n";
const { t } = useI18n();

const selectedLanguage = computed({
  get: () => languageStore.language,
  set: (value) => {
    tempLanguage.value = value;
  },
});

const languages = ref([
  { name: "English", code: "en" },
  { name: "Deutsch", code: "de" },
]);

// Temporary variable to store changes before saving
const tempLanguage = ref(languageStore.language);

// Dialog visibility
const visible = defineModel<boolean>({ required: true });

const closeDialog = () => {
  tempLanguage.value = languageStore.language;
  visible.value = false;
};

const saveSettings = () => {
  languageStore.setLanguage(tempLanguage.value);
  visible.value = false;
};
</script>
