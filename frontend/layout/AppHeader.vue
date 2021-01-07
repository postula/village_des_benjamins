<template>
  <header class="header-global">
    <base-nav class="navbar-main" transparent type="" effect="light" expand>
      <router-link slot="brand" class="navbar-brand mr-lg-5" to="/">
        <img src="static/brand/village_des_benjamins.png" alt="logo" />
      </router-link>

      <ul class="navbar-nav navbar-nav-hover align-items-lg-center">
        <li class="nav-item">
          <router-link to="/" class="nav-link nav-link-icon">
            Acceuil
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/reservation" class="nav-link nav-link-icon">
            Réservation
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/children" class="nav-link nav-link-icon">
            Enfants
          </router-link>
        </li>
      </ul>
      <ul class="navbar-nav align-items-lg-center ml-lg-auto">
        <li class="nav-item">
          <a
            class="nav-link nav-link-icon"
            href="https://www.facebook.com/Levillagedesbenjamins/"
            target="_blank"
            rel="noopener"
            data-toggle="tooltip"
            title="Aimez-nous sur Facebook"
          >
            <i class="fa fa-facebook-square"></i>
            <span class="nav-link-inner--text d-lg-none">Facebook</span>
          </a>
        </li>
        <template v-if="is_authenticated">
          <li class="nav-item">
            <a href="#" class="nav-link nav-link-icon" @click="logout">
              Déconnexion
            </a>
          </li>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link nav-link-icon">
            Connexion
          </router-link>
          <router-link to="/register" class="nav-link nav-link-icon">
            S'enregistrer
          </router-link>
        </template>
      </ul>
    </base-nav>
  </header>
</template>
<script>
import * as types from "../store/mutation-types";
import BaseNav from "@/components/BaseNav";

export default {
  components: {
    BaseNav,
  },
  computed: {
    is_authenticated() {
      return this.$store.getters.IsAuthenticated;
    },
  },
  methods: {
    logout() {
      this.$store.dispatch(types.LOGOUT);
    },
  },
};
</script>
<style>
</style>
