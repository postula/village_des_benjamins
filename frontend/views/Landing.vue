<template>
  <div>
    <div v-for="(section, index) in sections" :key="section.key">
        <Introduction v-if="section.layout === 'introduction'" :section="section"/>
        <SimpleList v-else-if="section.layout === 'simple_list'" :section="section" :items="contents.filter(c => c.section === section.key)" />
        <ListLeft v-else-if="section.layout === 'list_left'" :section="section" :items="contents.filter(c => c.section === section.key)" />
        <Team v-else-if="section.layout === 'team'" :section="section" />
        <Contact v-else-if="section.layout === 'contact'" :section="section" />
    </div>
  </div>
</template>

<script>
import Modal from "@/components/Modal.vue";
import BaseButton from "@/components/BaseButton";
import {Settings} from "luxon";
import * as types from "@/store/mutation-types";
import Introduction from "../layout/Introduction";
import ListRight from "../layout/ListRight";
import ListLeft from "../layout/ListLeft";
import SimpleList from "../layout/SimpleList";
import Team from "../layout/Team";
import Contact from "../layout/Contact";

export default {
  name: "home",
  components: {
    Introduction,
    Modal,
    BaseButton,
    ListLeft,
    SimpleList,
    Team,
    Contact,
  },
  data() {
    return {
      show_more: {
        section: null,
        id: null,
      }
    };
  },
  mounted() {
    Settings.defaultLocale = "fr";
    this.$store.dispatch(types.GET_CONTENTS);
    this.$store.dispatch(types.GET_SECTIONS);
  },
  methods: {
    showMore: function(section, contentId, evt) {
      evt.preventDefault();
      this.show_more.section = section;
      this.show_more.id = contentId;
    },
    hideMore: function(section, contentId, evt) {
      this.show_more.section = null;
      this.show_more.id = null;
    },
  },
  computed: {
    sections() {
      return this.$store.getters.getSections;
    },
    contents() {
      return this.$store.getters.getContents;
    },
  },
};
</script>


<style lang="scss">
#news_holder {
  max-height: 500px;
  overflow-y: auto;
}
</style>
