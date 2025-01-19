<<<<<<< HEAD
<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import LogIn from './components/LogIn.vue' // Führt zunächst zu Fehlermeldung, da TS nicht weiß, wie die .vue Datei zu verarbeiten ist. VSCode Neustart hilft. 

// Alternativ: "@/components/LogIn.vue" und im Script in der nächsten Zeile:
// export default {
//  name: 'LogIn',
// }
</script>

=======
>>>>>>> 889d83b1d765f3d1c31a52f44a220cdb30563ab9
<template>
  <!-- Lädt die Komponente in die Startseite -->
   <LogIn />
  <div>
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<style scoped></style>
