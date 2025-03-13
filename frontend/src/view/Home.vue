  <template>
    <Card>
      <template #title>Hangman</template>
      <template #content>
        <p class="m-0">
          Description for hangman game.
        </p>
      </template>
      <template #footer>
        <div class="flex gap-4 mt-1">
            <RouterLink to="/hangman">Open</RouterLink>
        </div>
      </template>
    </Card>
    <div>
      <RouterLink to="/example">Go to Example View</RouterLink>
    </div>
  </template>

  <script setup lang="ts">
  import { ref } from "vue";
  import { useToast } from "primevue/usetoast";

  const toast = useToast();
  </script>

  <style scoped></style>
