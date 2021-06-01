<template>
<div>
  <h2 class="mt-2 holiday_title text-xl">{{title}}</h2>
  <div class="list-group">
    <slot></slot>
  </div>
</div>
</template>

<script>
export default {
  name: "HolidaySection",
  props: {
    title: String,
  }
}
</script>

<style scoped>
.holiday_title {
  color: #e63e7d;
}
</style>
