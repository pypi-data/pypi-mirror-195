<script setup>
const props = defineProps({
  disabled: Boolean,
});

const emit = defineEmits(["enable-download"]);
</script>

<template>
  <button
    @click="emit('enable-download')"
    class="btn btn-lg btn-primary px-3 mb-4 z-3 shadow position-absolute bottom-0 start-50 translate-middle-x"
    :disabled="disabled"
  >
    <span class="button-text"
      ><i class="bi-download"></i><span class="mx-1"></span>Download All</span
    >
  </button>
</template>

<style scoped>
button {
  border-radius: 14px;
}
</style>
