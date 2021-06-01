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
                <small>S'enregistrer</small>
              </div>
              <form role="form">
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Prénom"
                  v-model="first_name"
                  addon-left-icon="ni ni-hat-3"
                  required
                  :error="errors.first_name"
                >
                </base-input>
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Nom"
                  v-model="last_name"
                  required
                  addon-left-icon="ni ni-hat-3"
                  :error="errors.last_name"
                >
                </base-input>
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Email"
                  v-model="email"
                  type="email"
                  required
                  :error="errors.email"
                  addon-left-icon="ni ni-email-83"
                >
                </base-input>
                <base-input
                  alternative
                  type="password"
                  placeholder="Mot de passe"
                  v-model="password"
                  required
                  :error="errors.password"
                  addon-left-icon="ni ni-lock-circle-open"
                >
                </base-input>
                <span v-if="!!errors.accept_newsletter" class="text-danger">
                  {{errors.accept_newsletter}}
                </span>
                <base-checkbox
                  alternative
                  v-model="accept_newsletter"
                  required
                  :error="errors.accept_newsletter"
                >
                  J'accepte de recevoir des notifications
                </base-checkbox>
                <div class="text-center">
                  <base-button type="primary" class="my-4" @click="signup"
                    >S'enregistrer</base-button
                  >
                </div>
              </form>
            </template>
          </card>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
import * as types from "@/store/mutation-types";

export default {
  data: () => ({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    accept_newsletter: false,
    errors: {
      first_name: "",
      last_name: "",
      email: "",
      password: "",
    },
  }),
  title: "Enregistrement",
  methods: {
    signup: function () {
      this.errors = {
      first_name: "",
      last_name: "",
      email: "",
      password: "",
    };
      let has_errors = false;
      if (! this.first_name) {
        has_errors = true;
        this.errors.first_name = "Ce champs est obligatoire";
      }
      if (! this.last_name) {
        has_errors = true;
        this.errors.last_name = "Ce champs est obligatoire";
      }
      if (! this.email) {
        has_errors = true;
        this.errors.email = "Ce champs est obligatoire";
      }
      if (! this.password) {
        has_errors = true;
        this.errors.password = "Ce champs est obligatoire";
      }
      if (! this.accept_newsletter) {
        has_errors = true;
        this.errors.accept_newsletter = "Ce champs est obligatoire";
      }
      if (has_errors) {
        return;
      }
      let info = {
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email.toLowerCase(),
        password: this.password,
        accept_newsletter: this.accept_newsletter,
      };


      this.$store
        .dispatch(types.REGISTER, info)
        .then(() => this.$router.push("/login"));
    },
  },
};
</script>
<style>
</style>
