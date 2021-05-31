<template>
<section class="section-profile-cover section-shaped my-0">
  <div class="shape shape-style-1 shape-default shape-skew alpha-4">
    <span v-for="n in dots" :key="n" />
  </div>
</section>
</template>

<script>
export default {
  name: "Skew",
  props: {
    dots: Number,
  }
}
</script>

<style scoped>

</style>
