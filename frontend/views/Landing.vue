<template>
  <div>

    <div class="position-relative">
      <!-- shape Hero -->
      <section class="section-shaped my-0">
        <div class="shape shape-style-1 shape-default shape-skew">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="container shape-container d-flex">
          <div class="col px-0">
            <div class="row">
              <div class="col-lg-6">
                <h1 class="display-3  text-white">{{ introductionSection.name }}</h1>
                <p class="lead  text-white">{{ introductionSection.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <!-- 1st Hero Variation -->
    </div>
    <section class="section section-lg pt-lg-0">
      <div class="container">
        <div class="row justify-content-center text-center mb-lg">
          <div class="col-lg-8">
            <h2 class="display-3">{{serviceSection.name}}</h2>
            <p class="mt-0">{{serviceSection.description}}</p>
          </div>
        </div>
        <div class="row justify-content-center">
          <div class="col-lg-12">
            <div class="row row-eq-height">
              <div class="col-lg-4 my-5" v-for="service in services" :key="service.id">
                <card class="border-0" hover shadow body-classes="py-5">
                  <icon v-show="service.icon" :name="`fa fa-${service.icon}`" type="primary" rounded class="mb-4">
                  </icon>
                  <h6 class="text-primary text-uppercase">{{ service.name }}</h6>
                  <p class="description mt-3">{{ service.description }}</p>
                </card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section section-shaped my-0 overflow-hidden">
      <div class="shape shape-style-1 bg-gradient-warning shape-skew">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
      <div class="container py-0">
        <div class="row row-grid align-items-center">
          <div class="col-md-6 order-lg-2 ml-lg-auto">
            <div class="position-relative pl-md-5">
              <img src="static/ill/ill-2.svg" class="img-center img-fluid">
            </div>
          </div>
          <div class="d-flex px-3">
            <div>
              <icon name="ni ni-building" size="lg" class="bg-gradient-white" color="primary" shadow
                    rounded></icon>
            </div>
            <div class="pl-4">
              <h2 class="display-3">{{objectivesSection.name}}</h2>
              <p class="text-white">{{ objectivesSection.description }}</p>
            </div>
          </div>

          <div class="col-lg-6 order-lg-1">
            <card shadow class="shadow-lg--hover mt-5" v-for="objective in objectives" :key="objective.id">
              <div class="d-flex px-3">
                <div>
                  <icon v-show="objective.icon" :name="`fa fa-${objective.icon}`" gradient="success" color="white"
                        shadow
                        rounded></icon>
                </div>
                <div class="pl-4">
                  <h5 class="title text-success">{{ objective.name }}</h5>
                  <p>{{ objective.description }}</p>
                </div>
              </div>
            </card>
          </div>
        </div>
      </div>
    </section>
    <section class="section section-lg">
      <div class="container">
        <div class="row justify-content-center text-center mb-lg">
          <div class="col-lg-8">
            <h2 class="display-3">{{teamSection.name}}</h2>
            <p class="mt-0">{{teamSection.description}}</p>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6 col-lg-3 mb-5 mb-lg-0" v-for="member in team_members" :key="member.id">
            <div class="px-4">
              <img :src="member.photo"
                   class="rounded-circle img-center img-fluid shadow shadow-lg--hover"
                   style="width: 200px;">
              <div class="pt-4 text-center">
                <h5 class="title">
                  <span class="d-block mb-1">{{ member.first_name }} {{ member.last_name }}</span>
                  <small class="h6 text-muted">{{ member.role }}</small>
                </h5>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="section section-shaped my-0 overflow-hidden">
      <div class="shape shape-style-3 bg-gradient-default shape-skew">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
      <div class="container pt-lg pb-300">
        <div class="row text-center justify-content-center">
          <div class="col-lg-10">
            <h2 class="display-3 text-white">{{methodologySection.name}}</h2>
            <p class="lead text-white">{{methodologySection.description}}</p>
          </div>
        </div>
        <div class="row row-grid mt-5">
          <div class="col-lg-4" v-for="methodologie in methodologies" :key="methodologie.id">
            <icon v-show="methodologie.icon" name="`fa fa-${methodologie.icon}" size="lg" gradient="white" shadow round color="primary"></icon>
            <h5 class="text-white mt-3">{{methodologie.name}}</h5>
            <p class="text-white mt-3">{{methodologie.description}}</p>
          </div>
        </div>
      </div>
    </section>
    <section class="section section-lg pt-lg-0 section-contact-us">
      <div class="container">
        <div class="row justify-content-center mt--300">
          <div class="col-lg-8">
            <card gradient="secondary" shadow body-classes="p-lg-5">
              <h4 class="mb-1">{{contactSection.name}}</h4>
              <p class="mt-0">{{contactSection.description}}</p>
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
            </card>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import {Settings} from "luxon";
import * as types from "@/store/mutation-types";

export default {
  name: "home",
  components: {},
  data() {
    return {
      contactName: "",
      contactMail: "",
      contactMessage: "",
      contactFeedback: "",
    };
  },
  mounted() {
    Settings.defaultLocale = "fr";
    this.$store.dispatch(types.GET_CONTENTS);
    this.$store.dispatch(types.GET_SECTIONS);
    this.$store.dispatch(types.GET_TEAM_MEMBERS);
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
  },
  computed: {
    sections() {
      return this.$store.getters.getSections;
    },
    services() {
      return this.$store.getters.getServices;
    },
    objectives() {
      return this.$store.getters.getObjectives;
    },
    methodologies() {
      return this.$store.getters.getMethodologies;
    },
    team_members() {
      return this.$store.getters.getTeamMembers;
    },
    introductionSection() {
      return this.sections.find(s => s.key === "introduction") || {}
    },
    serviceSection() {
      return this.sections.find(s => s.key === "service") || {}
    },
    objectivesSection() {
      return this.sections.find(s => s.key === "objectif") || {}
    },
    teamSection() {
      return this.sections.find(s => s.key === "team") || {}
    },
    methodologySection() {
      return this.sections.find(s => s.key === "methodologie") || {}
    },
    contactSection() {
      return this.sections.find(s => s.key === "contact") || {}
    },
  },
};
</script>
