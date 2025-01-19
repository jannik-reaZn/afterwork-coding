<template>
    <div>
        <input placeholder="Username" type="text" name="username" id="username">
        <input placeholder="Password" type="text" name="password" id="password">
    </div>
</template>

<script>
    export default {
        name: 'LogIn',
    }
</script>

<!-- Beschränkt den Style auf diese Datei -->
<style scoped> 
div {
    background-color: rgba(160, 100, 224, 0.034);
    display: flex;
    flex-direction: column;
    align-items: center;
}

input {
    border-width: 2px;
    border-style: solid;
    border-color: rgba(72, 9, 56, 0.524);
    border-radius: 5px;
}
</style>