<!-- src/components/dashboard/profesor/HistoricoEvaluaciones.vue -->
<template>
  <div class="space-y-6">

    <h1 class="text-2xl font-bold text-emerald-400">
      Histórico de Evaluaciones
    </h1>

    <p class="text-gray-300">
      <!-- Consulte todas las evaluaciones registradas por usted a lo largo del semestre.
      Próximamente podrá ver detalles por procedimiento, estudiante y fecha. -->
    </p>

    <!-- Tabla Placeholder -->
    <div class="bg-gray-800 p-6 rounded-2xl shadow-lg">

      <table class="w-full text-left">
        <thead class="text-emerald-400">
          <tr>
            <th class="py-2">Estudiante</th>
            <th>Procedimiento</th>
            <th>Nivel</th>
            <th>Fecha</th>
          </tr>
        </thead>

        <!-- Cuerpo idéntico al estudiante -->
        <tbody class="text-gray-300">
          <tr>
            <td class="py-2 text-center" colspan="4">
              (Aquí aparecerán los registros)
            </td>
          </tr>
        </tbody>

      </table>
    </div>

  </div>
</template>

<script setup>
// Vista placeholder — pendiente integración API
</script>
