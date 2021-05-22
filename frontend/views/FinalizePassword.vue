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
              <base-alert type="danger" v-if="error">
                {{error}}
              </base-alert>
              <base-alert type="success" v-if="feedback">
                {{feedback}}
              </base-alert>
              <form role="form">
                <base-input
                  alternative
                  type="password"
                  placeholder="Nouveau mot de passe"
                  v-model="password"
                  addon-left-icon="ni ni-lock-circle-open"
                >
                </base-input>
                <div class="text-center">
                  <base-button :disabled="!password" type="primary" class="my-4" @click="submit"
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
    feedback: "",
    password: "",
    token: "",
    error: "",
  }),
  created() {
    const token = this.$route.query.token;
    this.token = token;
    this.test_token(token);
  },
  methods: {
    async test_token(token) {
      const {success} = await this.$store.dispatch(types.VERIFY_FORGOT_PASSWORD_TOKEN, {token});
      if (!success) {
        this.error = "Le lien n'est pas valide";
      }
    },
    async submit() {
      const {success, error} = await this.$store.dispatch(types.RESET_PASSWORD, {
        password: this.password,
        token: this.token,
      });
      if (success) {
        this.feedback = "Votre mot de passe a été réinitialisé, vous pouvez maintenant vous connecter";
      } else {
        if (error === "Same password was set before") {
          this.error = "Vous ne pouvez pas réutiliser le même mot de passe."
        } else {
          this.error = error;
        }
      }
    },
  },
};
</script>
<style>
</style>
