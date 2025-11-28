<!-- src/components/estudiante/HistoricoProcedimientos.vue -->
<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-emerald-400">
      Histórico de Procedimientos
    </h1>

    <p class="text-gray-300">
      <!-- Consulta todos los procedimientos registrados, sus evaluaciones y tu progreso por semestre. -->
    </p>

    <!-- Tabla placeholder -->
    <div class="bg-gray-800 p-6 rounded-2xl shadow-lg">
      <table class="w-full text-left">
        <thead class="text-emerald-400">
          <tr>
            <th class="py-2">Fecha</th>
            <th>Procedimiento</th>
            <th>Nivel (Estudiante)</th>
            <th>Nivel (Profesor)</th>
            <th>Semestre</th>
          </tr>
        </thead>
        <tbody class="text-gray-300">
  <tr>
    <td class="py-2 text-center" colspan="5">
      (Aquí aparecerán los registros)
    </td>
  </tr>
</tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
// Pendiente: consumir API
</script>
