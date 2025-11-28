<template>
  <div class="p-6">
    <!-- #️⃣ Título dinámico -->
    <h1 class="text-2xl font-bold mb-4 text-emerald-400">{{ title }}</h1>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>
