<script setup>
import { computed } from "vue";

const props = defineProps({
  number: String,
  title: String,
  received: Number,
  total: Number,
});

const status = computed(() => {
  if (!props.number || !props.title) {
    return "Fetching";
  } else if (props.total == 0) {
    return "Ready";
  } else if (props.received < props.total) {
    return "Downloading";
  } else {
    return "Finished";
  }
});

const working = computed(() => {
  return ["Fetching", "Downloading"].includes(status.value);
});

const B2MiB = 1048576; // 1024 * 1024

const received_mib = computed(() => {
  return (props.received / B2MiB).toFixed(1);
});

const total_mib = computed(() => {
  return (props.total / B2MiB).toFixed(1);
});

const progress = computed(() => {
  if (status.value == "Downloading") {
    return Math.round((props.received / props.total) * 100);
  } else {
    return 100;
  }
});
</script>

<template>
  <div class="card w-100 shadow-sm">
    <div class="card-body position-relative">
      <h6 v-if="number" class="text-muted mb-1">{{ number }}</h6>
      <div v-else class="placeholder-wave">
        <h6 class="placeholder w-25 bg-secondary" style="height: 19px"></h6>
      </div>
      <h5 v-if="title" class="text-truncate">{{ title }}</h5>
      <div v-else class="placeholder-wave">
        <h5 class="placeholder w-75 bg-secondary" style="height: 24px"></h5>
      </div>
      <div class="progress">
        <div
          class="progress-bar"
          :class="{
            'progress-bar-striped': working,
            'progress-bar-animated': working,
            'bg-warning': status == 'Fetching',
            'bg-secondary': status == 'Ready',
            'bg-primary': status == 'Downloading',
            'bg-success': status == 'Finished',
          }"
          role="progressbar"
          :style="{ width: progress + '%' }"
        >
          <span v-if="status == 'Fetching'" class="text-dark"
            >Fetching Information</span
          >
          <span v-else-if="status == 'Ready'">Ready</span>
          <span v-else-if="status == 'Downloading'"
            >{{ progress }}%<span class="px-1"></span>({{ received_mib }} /
            {{ total_mib }} MiB)</span
          >
          <span v-else="status == 'Finished'">Download Complete</span>
        </div>
      </div>
      <i
        class="position-absolute end-0 top-50 translate-middle"
        :class="{
          'text-warning': status == 'Fetching',
          'bi-info-circle': status == 'Fetching',
          'text-secondary': status == 'Ready',
          'bi-slash-circle': status == 'Ready',
          'text-primary': status == 'Downloading',
          'bi-arrow-down-circle': status == 'Downloading',
          'text-success': status == 'Finished',
          'bi-check-circle': status == 'Finished',
        }"
      ></i>
    </div>
  </div>
</template>

<style scoped>
i {
  font-size: 36px;
}

.card-body {
  padding-right: 64px;
}
</style>
