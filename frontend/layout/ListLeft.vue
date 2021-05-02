<template>
  <section class="section section section-shaped my-0" :id="section.key">
  <div class="inversed_skew shape" :style="cssVars">
    <WhiteDot top="10%" left="5%" :opacity=".05"/>
    <WhiteDot top="15%" left="10%" :opacity=".10"/>
    <WhiteDot top="90%" left="15%" :opacity=".05"/>
    <WhiteDot top="95%" left="20%" :opacity=".10"/>
    <WhiteDot top="10%" left="95%" :opacity=".05"/>
    <WhiteDot top="56%" left="45%" :opacity=".10"/>
    <WhiteDot top="58%" left="56%" :opacity=".05"/>
  </div>
  <div class="container py-0" :id="section.key">
    <div class="row row-grid align-items-center">
      <div class="col-md-6 order-lg-2 ml-lg-auto">
        <div class="position-relative pl-md-5">
          <img :src="section.photo" class="img-center img-fluid">
        </div>
      </div>
      <div class="d-flex px-3">
        <div>
          <icon name="ni ni-building" size="lg" class="bg-gradient-white" color="primary" shadow
                rounded></icon>
        </div>
        <div class="pl-4">
          <h2 class="display-3">{{section.name}}</h2>
          <p class="text-white" v-html="section.description"></p>
        </div>
      </div>

      <div class="col-lg-6 order-lg-1">
        <card shadow class="shadow-lg--hover mt-5" v-for="item in ordered_items" :key="item.id">
          <div class="d-flex px-3">
            <div>
              <icon v-show="item.icon" :name="`fa fa-${item.icon}`" gradient="success" color="white"
                    shadow
                    rounded></icon>
            </div>
            <div class="pl-4">
              <h5 class="title text-success">{{ item.name }}</h5>
              <p v-html="item.description"></p>
              <base-button v-if="item.show_more_button" type="primary" @click="showMore(item.id, $event)">{{item.show_more_button}}</base-button>
              <modal v-if="item.show_more_button && item.show_more_content" @close="hideMore" :show="show_more_item === item.id">
                <template slot="header">
                  <h5 class="modal-title" >{{item.show_more_button}}</h5>
                </template>
                <div>
                  <div v-html="item.show_more_content"></div>
                </div>
              </modal>
            </div>
          </div>
        </card>
      </div>
    </div>
  </div>
</section>
</template>

<script>
import WhiteDot from "../components/WhiteDot";
import Modal from "../components/Modal";

const order_sort = (a, b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0);

export default {
  name: "ListLeft",
  components: {
    WhiteDot,
    Modal,
  },
  data() {
    return {
      show_more_item: null,
    };
  },
  methods: {
    showMore: function (contentId, evt) {
      evt.preventDefault();
      this.show_more_item = contentId;
    },
    hideMore: function (contentId, evt) {
      this.show_more_item = null;
    },
  },
  computed: {
    ordered_items() {
      return this.items.sort(order_sort);
    },
    cssVars() {
      return {
        "--background": this.section.background,
      };
    },
  },
  props: {
    section: Object,
    items: Array,
  }
}
</script>

<style scoped>

.inversed_skew {
  transform: skewY(-8deg);
  transform-origin: -180px;
      position: absolute;
    top: 0;
    z-index: -1;
    width: 100%;
    height: 100%;
  background: var(--background);
}
</style>
