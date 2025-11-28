<!-- src/components/estudiante/RetroalimentacionProfesor.vue -->
<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-emerald-400">
      Retroalimentación del Profesor
    </h1>

    <p class="text-gray-300">
      <!-- Aquí puedes consultar los comentarios que tus profesores han registrado sobre tus procedimientos. -->
    </p>

    <!-- Lista de retroalimentación -->
    <div class="bg-gray-800 p-6 rounded-2xl shadow-lg space-y-4">

      <div class="border border-gray-700 p-4 rounded-lg">
        <p class="text-sm text-gray-400">
          "Por favor, sea breve y preciso en sus comentarios sobre la actividad desarrollada por el estudiante."
        </p>

        <p class="mt-3 text-gray-300">
          (Aquí aparecerá la retroalimentación real)
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
// Pendiente: API para cargar evaluaciones
</script>
