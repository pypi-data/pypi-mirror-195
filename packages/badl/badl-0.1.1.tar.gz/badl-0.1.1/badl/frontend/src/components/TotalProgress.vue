<script setup>
import { computed } from "vue";

const props = defineProps({
  display: String,
  finished: Number,
  total: Number,
});

const progress = computed(() => {
  return Math.round((props.finished / props.total) * 100);
});
</script>

<template>
  <div class="shadow-lg bg-body px-3 pt-2 pb-3 border-top border-2 z-3">
    <div class="mb-1 text-center">
      {{ display }}<span class="px-2">-</span>{{ finished }} / {{ total }}
    </div>
    <div class="progress" role="progressbar">
      <div
        class="progress-bar progress-bar-striped progress-bar-animated"
        :style="{ width: progress + '%' }"
      ></div>
    </div>
  </div>
</template>

<style scoped>
.progress {
  height: 24px;
}
</style>
