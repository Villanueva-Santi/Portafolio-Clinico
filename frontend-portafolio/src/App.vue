<!-- src/App.vue -->
<template>
  <router-view class="w-screen h-screen" />
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
</style>
