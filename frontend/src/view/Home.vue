<template>
  <div class="card">
    <LogIn />
    <Button label="Create User" @click="createUser" />
    <button type="button" @click="increment">
      count is {{ counterStore.count }}
    </button>
  </div>
  <div>
    <RouterLink to="/example">Go to Example View</RouterLink>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useCounterStore } from "@/store/counter";
import { useItemStore } from "@/store/item";
import { useToast } from "primevue/usetoast";
import LogIn from "@/components/LogIn.vue";

const counterStore = useCounterStore();
const itemStore = useItemStore();
const toast = useToast();

const increment = () => {
  counterStore.increment();
};

const item = ref({
  name: "Test Item",
  description: "This is a test item",
  price: 10.99,
  is_available: true,
});

const createUser = async () => {
  try {
    await itemStore.addItem(item.value);
    toast.add({
      severity: "info",
      summary: "Info",
      detail: "Successfully created user",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Info",
      detail: "An error occured while creating a user",
      life: 3000,
    });
  }
};
</script>

<style scoped></style>
