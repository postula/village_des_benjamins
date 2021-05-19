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
                <small>Connexion</small>
              </div>
              <form role="form">
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Email"
                  v-model="credentials.email"
                  addon-left-icon="ni ni-email-83"
                >
                </base-input>
                <base-input
                  alternative
                  type="password"
                  placeholder="Mot de passe"
                  v-model="credentials.password"
                  addon-left-icon="ni ni-lock-circle-open"
                >
                </base-input>
                <div class="text-center">
                  <base-button type="primary" class="my-4" @click="login()"
                    >Se Connecter</base-button
                  >
                </div>
              </form>
            </template>
          </card>
          <div class="row mt-3">
            <div class="col-6">
              <a href="#" class="text-light">
                <small>Mot de passe oublié?</small>
              </a>
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
  title: "Connexion",
  data: () => ({
    credentials: {
      email: "",
      password: "",
    },
    error: "",
  }),
  methods: {
    login() {
      const credentials = {
        email: this.credentials.email,
        password: this.credentials.password,
      };
      let redirect = decodeURIComponent(this.$route.query.redirect || "/");
      this.$store.dispatch(types.UPDATE_TOKEN, {
        credentials: credentials,
        redirect: redirect,
      });
    },
  },
};
</script>
<style>
</style>
