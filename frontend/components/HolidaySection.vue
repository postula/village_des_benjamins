<template>
<div>
  <h4 class="mt-2">{{title}}</h4>
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

</style>
