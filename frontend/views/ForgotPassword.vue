<template>
  <section class="section section-shaped section-lg my-0">
    <div class="shape shape-style-1 bg-gradient-default">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="container pt-lg-md">
      <div class="row justify-content-center">
        <div class="col-lg-5">
          <card
            type="secondary"
            shadow
            header-classes="bg-white pb-5"
            body-classes="px-lg-5 py-lg-5"
            class="border-0"
          >
            <template>
              <div class="text-center text-muted mb-4">
                <small>Oubli de mot de passe</small>
              </div>
              <base-alert type="success" v-if="feedback">
                {{feedback}}
              </base-alert>
              <form role="form">
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Email"
                  v-model="email"
                  addon-left-icon="ni ni-email-83"
                >
                </base-input>
                <div class="text-center">
                  <base-button type="primary" class="my-4" @click="submit"
                    >Réinitialiser</base-button
                  >
                </div>
              </form>
            </template>
          </card>
          <div class="row mt-3">
            <div class="col-6">
              <router-link to="login" class="text-light">
                <small>Connexion</small>
              </router-link>
            </div>
            <div class="col-6 text-right">
              <router-link to="register" class="text-light">
                <small>Créer un compte</small>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
import * as types from "../store/mutation-types";
export default {
  title: "Mot de passe oublié",
  data: () => ({
    email: "",
    feedback: "",
  }),
  methods: {
    async submit() {
      await this.$store.dispatch(types.FORGOT_PASSWORD, {
        email: this.email,
      });
      this.feedback = "Si l'adresse est connue de nos systèmes, un email avec les instructions vous ont été envoyées";
    },
  },
};
</script>
<style>
</style>
