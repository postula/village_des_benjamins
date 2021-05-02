<template>
<section class="section section-lg pt-lg-0 section-contact-us" :id="section.key">
      <div class="container">
        <div class="row justify-content-center mt--300">
          <div class="col-lg-10">
            <card gradient="secondary" shadow body-classes="p-lg-8">
              <div class="row">
              <div class="col-lg-8">
                <h4 class="mb-1">{{section.name}}</h4>
                <p class="mt-0" v-html="section.description"></p>
                <base-alert v-if="contactFeedback" type="success">
                  {{contactFeedback}}
                </base-alert>
                <base-input class="mt-5"
                            alternative
                            required
                            placeholder="Votre nom"
                            v-model="contactName"
                            addon-left-icon="ni ni-user-run">
                </base-input>
                <base-input alternative
                            placeholder="Adresse électronique"
                            required
                            type="email"
                            v-model="contactMail"
                            addon-left-icon="ni ni-email-83">
                </base-input>
                <base-input class="mb-4">
                                      <textarea v-model="contactMessage" required class="form-control form-control-alternative" name="name" rows="4"
                                                cols="80" placeholder="Votre message..."></textarea>
                </base-input>
                <base-button type="default" round block size="lg" @click="sendMessage">
                  Envoyer
                </base-button>
              </div>
              <div class="col-lg-4">
                <MapContainer />
              </div>
                </div>

            </card>
          </div>
        </div>
      </div>
    </section>
</template>

<script>
import * as types from "@/store/mutation-types";
import BaseButton from "@/components/BaseButton";
import BaseInput from "@/components/BaseInput";
import MapContainer from "../components/MapContainer";
export default {
  name: "Contact",
  components: {
    MapContainer,
    BaseButton,
    BaseInput,
  },
  props: {
    section: Object,
  },
  data() {
    return {
      contactName: "",
      contactMail: "",
      contactMessage: "",
      contactFeedback: "",
    }
  },
  methods: {
    sendMessage() {
      const payload = {
        name: this.contactName,
        email: this.contactMail,
        message: this.contactMessage,
      }
      this.$store.dispatch(types.CREATE_MESSAGE, payload);
      this.contactName = "";
      this.contactMail = "";
      this.contactMessage = "";
      this.contactFeedback = "Votre message a bien été envoyé";
    }
  }
}
</script>

<style scoped>

</style>
