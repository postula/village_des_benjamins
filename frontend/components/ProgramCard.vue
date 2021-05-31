<template>
  <div
      class="list-group-item list-group-item-action flex-column align-items-start"
  >
    <div
        class="d-flex w-100 justify-content-center justify-content-md-between flex-wrap flex-sm-column flex-md-row"
    >
      <div class="d-flex flex-sm-column flex-md-row">
        <i class="fa fa-calendar mr-1"/>
        <span>{{ start_date_str }}</span>
        <span> - </span>
        <span>{{ end_date_str }}</span>
      </div>
      <div class="d-flex justify-content-between">
        <span class="mr-1" v-for="({first_name, id}, index) in educators" :key="id">
          {{ first_name }}
          <span v-if="index !== (educators.length - 1)"> & </span>
        </span>
      </div>
    </div>
    <div>
      <h5 class="mt-1 mb-1">
        {{ theme }}
      </h5>
    </div>
    <p class="description" v-html="description" v-if="description"></p>
    <div class="d-flex flex-column flex-md-row justify-content-between">
      <div v-if="bricolage" title="Bricolages" class="my-2 my-md-0 font-weight-normal">
        <i class="fa fa-cubes mr-1"/>{{ bricolage }}
      </div>
      <div v-if="food" title="Activités Culinaires" class="my-2 my-md-0 font-weight-normal">
        <i class="fa fa-cutlery mr-1"/>{{ food }}
      </div>
      <div v-if="game" title="Jeux" class="my-2 my-md-0 font-weight-normal">
        <i class="fa fa-gamepad mr-1"/>{{ game }}
      </div>
      <div v-if="other" title="Divers" class="my-2 my-md-0 font-weight-normal">
        <i class="fa fa-magic mr-1"/>{{ other }}
      </div>
    </div>
  </div>
</template>

<script>
import {formatDate} from "@/utils";

export default {
  name: "ProgramCard",
  props: {
    start_date: String,
    end_date: String,
    educators: Array,
    theme: String,
    description: String,
    bricolage: String,
    food: String,
    game: String,
    other: String,
  },
  computed: {
    start_date_str() {
      return formatDate(this.start_date);
    },
    end_date_str() {
      return formatDate(this.end_date);
    },
  }
}
</script>

<style scoped>

</style>
