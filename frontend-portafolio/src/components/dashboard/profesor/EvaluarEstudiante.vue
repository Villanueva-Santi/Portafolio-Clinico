<!-- src/components/dashboard/profesor/EvaluarEstudiante.vue -->
<template>
  <div class="space-y-6">
    
    <!-- Título -->
    <h1 class="text-2xl font-bold text-emerald-400">
      Retroalimentar Estudiante
    </h1>

    <!-- Mensaje superior 
    <p class="text-gray-300 max-w-2xl text-left">
      Registre la evaluación del procedimiento clínico realizado por el estudiante.
      <br />
      <span class="text-emerald-400 font-semibold">
        Por favor sea breve y preciso en sus comentarios sobre la actividad desarrollada por el estudiante.
      </span>
    </p> -->

    <!-- 📌 Card principal -->
    <div class="bg-gray-800 p-6 rounded-2xl shadow-lg space-y-4">

      <!-- Estudiante -->
      <div>
        <label class="block text-sm mb-1">Seleccione Estudiante</label>
        <select
          v-model="form.estudiante"
          class="w-1/2 p-2 rounded bg-gray-700 text-white"
        >
          <option value="">-- Seleccione un estudiante --</option>
          <option>(Futuro) Estudiante 01</option>
          <option>(Futuro) Estudiante 02</option>
        </select>
      </div>
      
      <!-- Fecha -->
      <div>
        <label class="block text-sm mb-1">Fecha</label>
        <input
          type="date"
          v-model="form.fecha"
          class="w-1/5 p-2 rounded bg-gray-700 text-white"
        />
      </div>

      <!-- Procedimiento -->
      <div>
        <label class="block text-sm mb-1">Procedimiento Clínico</label>
        <select
          v-model="form.procedimiento"
          class="w-1/4 p-2 rounded bg-gray-700 text-white"
        >
          <option value="">-- Seleccione un procedimiento --</option>
          <option>Sutura</option>
          <option>Cirugía</option>
          <option>Consulta Externa</option>
        </select>
      </div>

      <!-- Nivel Dreyfus + descripción dinámica -->
      <div class="flex items-start gap-6">
        <div>
          <label class="block text-sm mb-1">Nivel de Desempeño (Modelo Dreyfus y Dreyfus)</label>

          <select
            v-model="form.nivel"
            class="w-60 p-2 rounded bg-gray-700 text-white"
          >
            <option value="">-- Seleccione un nivel --</option>
            <option value="NOVATO">Novato</option>
            <option value="PRINCIPIANTE_AVANZADO">Principiante Avanzado</option>
            <option value="COMPETENTE">Competente</option>
            <option value="PROFESIONAL">Profesional</option>
            <option value="EXPERTO">Experto</option>
          </select>
        </div>

        <!--  Cuadro dinámico -->
        <div
          v-if="descripcionNivel"
          class="w-full p-4 rounded-xl bg-gray-700 text-white border border-gray-500 shadow leading-relaxed space-y-2"
          v-html="descripcionNivel"
        ></div>
      </div>

      <!-- Retroalimentación -->
      <div>
        <label class="block text-sm mb-1">Comentarios al Estudiante</label>
        <textarea
          v-model="form.retroalimentacion"
          class="w-full p-3 rounded bg-gray-700 text-white"
          rows="4"
          placeholder="Por favor, realice comentarios útiles para fortalecer el desempeño del estudiante..."
        ></textarea>
      </div>

      <!-- Botón -->
      <button
        class="w-full bg-emerald-600 hover:bg-emerald-700 text-white py-2 rounded transition"
        @click="confirmarGuardado"
      >
        Guardar Retroalimentación
      </button>
    </div>

    <!-- CONFIRMACIÓN -->
    <div
      v-if="mostrarConfirmacion"
      class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center"
    >
      <div class="bg-gray-800 p-6 rounded-xl shadow-xl text-white space-y-4 w-96 text-center">
        <h2 class="text-lg font-semibold">Confirmar Retroalimentación</h2>
        <p>¿Seguro que deseas registrar esta retroalimentación?</p>

        <div class="flex justify-between mt-4">
          <button
            class="px-4 py-2 bg-red-600 rounded hover:bg-red-700"
            @click="mostrarConfirmacion = false"
          >
            Cancelar
          </button>

          <button
            class="px-4 py-2 bg-emerald-600 rounded hover:bg-emerald-700"
            @click="guardarEvaluacion"
          >
            Confirmar
          </button>
        </div>
      </div>
    </div>

    <!-- ÉXITO -->
    <div
      v-if="mostrarExito"
      class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center"
    >
      <div class="bg-gray-800 p-6 rounded-xl shadow-xl text-white space-y-4 w-96 text-center">
        <h2 class="text-lg font-semibold">Retroalimentación Registrada</h2>
        <p>La retroalimentación se ha guardado correctamente.</p>
        <button
          class="px-4 py-2 bg-emerald-600 rounded hover:bg-emerald-700 w-full"
          @click="mostrarExito = false"
        >
          OK
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";   

// Formulario reactivo
const form = ref({
  estudiante: "",
  procedimiento: "",
  nivel: "",
  retroalimentacion: "",
});

const descripciones = {
  NOVATO: `
<strong>Novato:</strong> Este nivel se caracteriza por la falta de experiencia y conocimientos en una determinada área. 
Los novatos requieren instrucciones y reglas explícitas para llevar a cabo tareas, además de orientación por parte del profesor. 
<br>
<br>
<hr />
<br>
• Sigue reglas estrictas, descontextualizadas y literales.<br>
• No reconoce patrones; depende completamente del manual o del docente.<br>
• Actúa paso a paso, sin priorizar información.<br>
• En medicina: Corresponde al estudiante que necesita guías claras, listas de chequeo y supervisión directa.	
  `,
  PRINCIPIANTE_AVANZADO: `
<strong>Principiante Avanzado:</strong> En este nivel, los individuos tienen alguna experiencia práctica en el área y pueden 
empezar a tomar decisiones por sí mismos, aunque aún requieren reglas claras y orientación del profesor.
<br>
<br>
<hr />
<br>
• Comienza a identificar situaciones recurrentes o <strong>“Aspectos relevantes”</strong>.<br>
• Reconoce patrones simples.<br>
• Toma decisiones básicas con apoyo.<br>
• En medicina: Realiza tareas estructuradas con guía.
  `,
  COMPETENTE: `
<strong>Competente:</strong> Las personas en este nivel tienen suficiente experiencia práctica para tomar decisiones sin 
necesidad de seguir reglas explícitas. Son capaces de resolver problemas comunes y realizar tareas de manera eficiente.
<br>
<br>
<hr />
<br>
• Organiza la información, prioriza y planifica acciones.<br>
• Toma decisiones deliberadas y responsables.<br>
• Gestiona casos clínicos comunes.<br>
• En medicina: Puede llevar un caso completo, justificar decisiones y reflexionar sobre errores.
  `,
  PROFESIONAL: `
<strong>Profesional:</strong> Las personas alcanzan un alto nivel de experiencia práctica, lo que les permite adaptarse a 
situaciones imprevistas y manejar tareas complejas con éxito.
<br>
<br>
<hr />
<br>
• Percibe la situación de manera holística (Integral).<br>
• Aplica las reglas con flexibilidad y empieza a utilizar la intuición basada en la experiencia.<br>
• Anticipa problemas y adapta planes de acción.<br>
• En medicina: Resuelve casos complejos, integra múltiples protocolos y orienta a otros profesionales.
  `,
  EXPERTO: `
<strong>Experto:</strong> En este nivel, las personas tienen un conocimiento profundo y una amplia experiencia en el área que 
les permite tomar decisiones intuitivas y creativas en situaciones complejas.
<br>
<br>
<hr />
<br>
• Toma decisiones de forma fluida, automática e intuitiva.<br>
• Las reglas ya no guían su acción; actúa con base en modelos mentales profundos.<br>
• Reconoce patrones sutiles y responde rápidamente sin análisis explícito.<br>
• En medicina: Corresponde a un clínico altamente competente, líder y referente, con elevada conciencia situacional.
  `,
};

// Descripción dinámica según selección
const descripcionNivel = computed(() => descripciones[form.value.nivel] || "");

// Estados de modales
const mostrarConfirmacion = ref(false);
const mostrarExito = ref(false);

// Abrir modal
const confirmarGuardado = () => {
  mostrarConfirmacion.value = true;
};

// Guardar evaluación (Mock)
const guardarEvaluacion = async () => {
  mostrarConfirmacion.value = false;

  try {
    console.log("Evaluación enviada:", form.value);
    mostrarExito.value = true;
  } catch (error) {
    console.error("❌ Error al guardar evaluación:", error);
    alert("Hubo un error guardando la evaluación.");
  }
};
</script>
