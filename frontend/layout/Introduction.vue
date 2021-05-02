<template>
<section class="section-shaped my-0">
    <div class="shape shape-style-1  shape-skew introduction">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="container shape-container d-flex">
      <div class="col px-0">
        <div class="row">
          <div class="col-lg-8">
            <h1 class="display-1  text-white">{{ section.name }}</h1>
            <p class="lead  text-white" v-html="section.description"></p>
          </div>
          <div class="card col-lg-4 px-0">
            <div class="card-header">
              Actualités
            </div>
            <div class="card-body" id="news_holder">
              <card class="border-0" v-for="news_item in news" :key="news_item.id">
                <h6 class="text-primary text-uppercase">{{news_item.date}}</h6>
                <p class="description mt-3" v-html="news_item.description"></p>
              </card>
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
  name: "Introduction",
  props: {
    section: Object,
  },
  mounted() {
    this.$store.dispatch(types.GET_NEWS);
  },
  computed: {
    news() {
      return this.$store.getters.getNews;
    }
  }
}
</script>

<style scoped>
.shape-skew.introduction {
  background: linear-gradient(180deg, #e63e7d 15%, #e53737 70%, #ee2134 94%);
}
</style>
