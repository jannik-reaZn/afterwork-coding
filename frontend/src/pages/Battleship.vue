<template>
  <div class="flex flex-1 text-center">
    <div class="w-full">
      <!-- Header -->
      <GameHeader @help-click="showDialog = true">
        <template #title>
          {{ $t("battleship.title") }}
        </template>
        <template #help-dialog>
          <BattleshipHelpDialog v-model:visible="showDialog" />
        </template>
      </GameHeader>

      <!-- Battleships -->
      <div class="flex items-center justify-center gap-4">
        <Battleship
          v-for="ship in availableShips"
          :key="ship.id"
          :id="ship.id"
          :size="ship.size"
          :orientation="ship.orientation"
        />
      </div>

      <!-- Game Board -->
      <div class="flex items-center justify-center pt-4">
        <BattleshipGameBoard :size="10" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";

import GameHeader from "@/components/GameHeader.vue";
import BattleshipHelpDialog from "@/components/battleship/BattleshipHelpDialog.vue";
import Battleship from "@/components/battleship/Battleship.vue";
import BattleshipGameBoard from "@/components/battleship/BattleshipGameBoard.vue";
import { Orientation } from "@/models/battleship/battleshipOrientation";

const showDialog = ref(false);

// Available ships to drag
const availableShips = reactive([
  { id: 1, size: 3, orientation: Orientation.Horizontal },
  { id: 2, size: 4, orientation: Orientation.Vertical },
]);
</script>
