<template>
  <section class="section section-shaped my-0" :id="section.key">
      <div class="shape shape-style-3 shape-skew" :style="cssVars">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
      <div class="container team">
        <div class="row justify-content-center text-center mb-lg">
          <div class="col-lg-8 text-white">
            <h2 class="display-3 text-white">{{section.name}}</h2>
            <p class="mt-0" v-html="section.description"></p>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6 col-lg-3 mb-5 mb-lg-0" v-for="member in team_members" :key="member.id">
            <div class="px-4">
              <img :src="member.photo"
                   class="rounded-circle img-center img-fluid shadow shadow-lg--hover"
                   style="width: 200px;">
              <div class="pt-4 text-center">
                <h5 class="title">
                  <span class="d-block mb-1 text-white">{{ member.first_name }} {{ member.last_name }}</span>
                  <small class="h6 text-muted text-white">{{ member.role }}</small>
                </h5>
              </div>
            </div>
          </div>
        </div>
      </div>
  </section>
</template>

<script>
import * as types from "@/store/mutation-types";
export default {
  name: "Team",
  props: {
    section: Object,
  },
  mounted() {
    this.$store.dispatch(types.GET_TEAM_MEMBERS);
  },
  computed: {
    team_members() {
      return this.$store.getters.getTeamMembers;
    },
    cssVars() {
      return {
        "--background": this.section.background,
      };
    },
  }
}
</script>

<style scoped>
.section-shaped .shape + .team.container {
  padding-bottom: 250px;
}
.section-shaped .shape.shape-skew {
  background-color: var(--background);
  transform-origin: -180px;
      position: absolute;
    top: 0;
}

</style>
