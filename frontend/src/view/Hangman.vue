<template>
    <h1>Hangman</h1>
    <div class="grid gap-2">
        <Button
            v-for="letter in alphabet"
            :key="letter"
            :label="letter"
            class="p-2"
        />
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const value = ref("");


const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("")
</script>

<style scoped>
</style>