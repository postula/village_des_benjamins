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
                >
                </base-input>
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Nom"
                  v-model="last_name"
                  addon-left-icon="ni ni-hat-3"
                >
                </base-input>
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Email"
                  v-model="email"
                  addon-left-icon="ni ni-email-83"
                >
                </base-input>
                <base-input
                  alternative
                  type="password"
                  placeholder="Mot de passe"
                  v-model="password"
                  addon-left-icon="ni ni-lock-circle-open"
                >
                </base-input>
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
export default {
  data: () => ({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  }),
  methods: {
    signup: function () {
      let info = {
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email,
        password: this.password,
      };

      this.$store
        .dispatch("signup", info)
        .then(() => this.$router.push("/login"));
    },
  },
};
</script>
<style>
</style>
