import { defineStore } from "pinia";
import { ref } from "vue";
import { createItem } from "@/api/itemService";

export const useItemStore = defineStore("itemStore", () => {
  const items = ref<any[]>([]);

  const addItem = async (payload: {
    name: string;
    description: string;
    price: number;
    is_available: boolean;
  }) => {
    try {
      const newItem = await createItem(payload);
      items.value.push(newItem);
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  };

  return { items, addItem };
});
