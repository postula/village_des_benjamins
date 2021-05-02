<template>
  <span id="a" :style="cssVars"></span>
</template>

<script>
export default {
  name: "WhiteDot",
  props: ["opacity", "top", "left"],
  computed: {
    cssVars() {
      return {
        "--opacity": this.opacity,
        "--top": this.top,
        "--left": this.left,
      }
    }
  }
}
</script>

<style scoped>
#a {
  height: 120px;
  width: 120px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, var(--opacity));
  top: var(--top);
  left: var(--left);
  position: absolute;
}
</style>
