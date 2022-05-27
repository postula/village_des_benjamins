<template>
  <div class="list-group-item list-group-item-action flex-column align-items-start">
    <div class="d-flex w-100 justify-content-center justify-content-md-between flex-wrap">
      <h5 class="mb-1">{{ name }}</h5>
      <div class="d-flex justify-content-between flex-column align-items-center align-items-md-end">
        <span>
          <i class="fa fa-calendar mr-1"/>
          {{start_date_str}}
          <span v-if="end_date_str">
            - {{ end_date_str }}
          </span>
        </span>
        <span v-if="departure_time && arrival_time">
          <i class="fa fa-hourglass mr-1"/>
          {{departure_time_str}}-{{arrival_time_str }}
        </span>
        <span>{{ price }} €</span>
        <span v-if="transport">{{ transport }}</span>
      </div>
    </div>
    <div>
      <p class="description" v-html="description" />
    </div>
  </div>
</template>

<script>
import {formatDate, formatTime} from "@/utils";

export default {
  name: "Outing",
  props: {
    name: String,
    start_date: String,
    end_date: String,
    arrival_time: String,
    departure_time: String,
    price: String,
    transport: String,
    description: String,
  },
  computed: {
    start_date_str() {
      return formatDate(this.start_date);
    },
    end_date_str() {
      return this.end_date && formatDate(this.end_date);
    },
    arrival_time_str() {
      return this.arrival_time && formatTime(this.arrival_time);
    },
    departure_time_str() {
      return this.departure_time && formatTime(this.departure_time);
    },
  }
}
</script>

<style scoped>

</style>
