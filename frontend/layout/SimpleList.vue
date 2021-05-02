<template>
  <section class="section section-lg pt-lg-0" :id="section.key">
    <div class="inversed_skew shape" :style="cssVars">
      <WhiteDot top="10%" left="5%" :opacity=".05"/>
      <WhiteDot top="15%" left="10%" :opacity=".10"/>
      <WhiteDot top="90%" left="15%" :opacity=".05"/>
      <WhiteDot top="95%" left="20%" :opacity=".10"/>
      <WhiteDot top="10%" left="95%" :opacity=".05"/>
      <WhiteDot top="56%" left="45%" :opacity=".10"/>
      <WhiteDot top="58%" left="56%" :opacity=".05"/>
    </div>
    <div class="container">
      <div class="row justify-content-center text-center mb-lg text-white">
        <div class="col-lg-8">
          <h2 class="display-3 text-white">{{section.name}}</h2>
          <p class="mt-0" v-html="section.description"></p>
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col-lg-12">
          <div class="row row-eq-height">
            <div class="col-lg-4 my-5" v-for="item in ordered_items" :key="item.id">
              <card class="border-0 h-100" shadow body-classes="py-5">
                <icon v-show="item.icon" :name="`fa fa-${item.icon}`" type="primary" rounded class="mb-4">
                </icon>
                <h6 class="text-primary text-uppercase">{{ item.name }}</h6>
                <p class="description mt-3" v-html="item.description"></p>
                <base-button v-if="item.show_more_button" type="primary" @click="showMore(item.id, $event)">{{item.show_more_button}}</base-button>
                <modal v-if="item.show_more_button && item.show_more_content" @close="hideMore" :show="show_more_item === item.id">
                  <template slot="header">
                    <h5 class="modal-title">{{item.show_more_button}}</h5>
                  </template>
                  <div>
                    <div v-html="item.show_more_content"></div>
                  </div>
                </modal>
              </card>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Modal from "@/components/Modal.vue";
import WhiteDot from "@/components/WhiteDot";
const order_sort = (a, b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0);

export default {
  name: "SimpleList",
  components: {
    Modal,
    WhiteDot
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
    hideMore: function () {
      this.show_more_item = null;
    },
  },
  computed: {
    cssVars() {
      return {
        "--background": this.section.background,
      };
    },
    ordered_items() {
      return this.items.sort(order_sort);
    }
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
