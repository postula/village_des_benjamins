<template>
  <div class="profile-page">
    <section class="section-profile-cover section-shaped my-0">
      <div class="shape shape-style-1 shape-default shape-skew alpha-4">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
    </section>
    <section class="section section-skew">
      <div class="container">
        <card shadow class="card-profile mt--300" no-body>
          <div class="px-4">
            <div class="row justify-content-center">
              <div class="col-lg-3 order-lg-2">
                <div class="card-profile-image">
                  <a href="#" @click="pictureModal">
                    <img :src="currentUser.photo" class="rounded-circle" />
                  </a>
                </div>
              </div>
              <div
                class="col-lg-4 order-lg-3 text-lg-right align-self-lg-center"
              ></div>
              <div class="col-lg-4 order-lg-1 d-none d-md-block">
                <div class="card-profile-stats d-flex justify-content-center">
                  <div>
                    <span class="heading">{{ numberOfChildren }}</span>
                    <span class="description"
                      >Enfant{{ numberOfChildren > 1 ? "s" : "" }}</span
                    >
                  </div>
                </div>
              </div>
            </div>
            <div class="text-center mt-5">
              <h3>{{ currentUser.first_name }} {{ currentUser.last_name }}</h3>
              <div class="h6 font-weight-300">
                {{ currentUser.email }}
              </div>
            </div>
            <div class="mt-5 py-5 border-top text-center">
              <div class="row justify-content-center">
                <div class="col-lg-9">
                  <div class="d-block d-md-none list-group">
                    <div
                      v-for="child in children"
                      :key="child.id"
                      class="list-group-item list-group-item-action flex-column align-items-start"
                    >
                      <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">
                          {{ child.first_name }} {{ child.last_name }}
                        </h5>
                        <small
                          ><i
                            :class="{
                              fa: true,
                              'fa-mars': child.gender == 'male',
                              'fa-venus': child.gender == 'female',
                            }"
                        /></small>
                      </div>
                      <div class="d-flex w-100 mt-2 justify-content-between">
                        <span>
                          <i class="fa fa-birthday-cake" />
                          {{ child.birth_date }}
                        </span>
                        <small>{{
                          child.section || "Pas de groupe disponible"
                        }}</small>
                      </div>
                      <div class="d-flex w-100 mt-2 justify-content-between">
                        <base-button
                          outline
                          type="warning"
                          icon="fa fa-pencil"
                          @click="editChildForm(child.id)"
                          >Modifier</base-button
                        >
                        <base-button
                          outline
                          type="danger"
                          icon="fa fa-trash"
                          @click="removeChildForm(child.id)"
                          >Retirer</base-button
                        >
                      </div>
                    </div>
                  </div>
                  <div class="d-none d-md-block">
                    <table v-if="numberOfChildren > 0" class="table">
                      <thead>
                        <tr>
                          <th scope="col">Prénom</th>
                          <th scope="col">Nom</th>
                          <th scope="col">Date de naissance</th>
                          <th scope="col">Sexe</th>
                          <th scope="col">Groupe</th>
                          <th scope="col">Statut</th>
                          <th scope="col"></th>
                          <th scope="col"></th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="child in children" :key="child.id">
                          <td class="align-middle">{{ child.first_name }}</td>
                          <td class="align-middle">{{ child.last_name }}</td>
                          <td class="align-middle">
                            {{ child.birth_date }}
                          </td>
                          <td class="align-middle">
                            <i
                              v-if="child.gender == 'male'"
                              class="fa fa-mars"
                            ></i>
                            <i v-else class="fa fa-venus"></i>
                          </td>
                          <td class="align-middle">
                            {{ child.section || "Pas de groupe disponible" }}
                          </td>
                          <td class="align-middle">
                            {{child_statuses[child.status]}}
                          </td>
                          <td>
                            <base-button
                              outline
                              type="warning"
                              icon="fa fa-pencil"
                              @click="editChildForm(child.id)"
                            ></base-button>
                          </td>
                          <td>
                            <base-button
                              outline
                              type="danger"
                              icon="fa fa-trash"
                              @click="removeChildForm(child.id)"
                            ></base-button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              <div class="row justify-content-center mt-5">
                <div class="col-lg-9">
                  <button class="btn btn-primary" @click="addChildForm">
                    Ajouter un enfant
                  </button>
                </div>
              </div>
              <modal :show.sync="modal.show">
                <template slot="header">
                  <h5>
                    <template v-if="modal.action == 'add'"
                      >Ajouter un enfant</template
                    >
                    <template v-else-if="modal.action == 'update'"
                      >Modifier un enfant</template
                    >
                    <template v-else-if="modal.action == 'delete'"
                      >Retirer un enfant</template
                    >
                  </h5>
                </template>
                <div>
                  <div v-if="modal.action == 'delete'">
                    Êtes-vous sûr de vouloir retirer
                    {{ modal.child.first_name }} {{ modal.child.last_name }} de
                    la liste?
                  </div>
                  <div v-else class="text-left">
                    <div class="row justify-content-center text-left">
                      <div class="col-lg-9">
                        <base-input
                          v-model="modal.child.first_name"
                          label="Prénom"
                          placeholder="Prénom"
                          required
                          :error="modal.errors.first_name"
                        ></base-input>
                        <base-input
                          v-model="modal.child.last_name"
                          label="Nom"
                          placeholder="Nom"
                          required
                          :error="modal.errors.last_name"
                        ></base-input>
                        <base-input
                          label="Sexe"
                          placeholder="Sexe"
                          required
                          :error="modal.errors.gender"
                          ><select
                            v-model="modal.child.gender"
                            class="form-control"
                          >
                            <option value="male">Garçon</option>
                            <option value="female">Fille</option>
                          </select></base-input
                        >
                        <base-input
                          label="Date de naissance"
                          required
                          :error="modal.errors.birth_date"
                        >
                          <flat-picker
                            slot-scope="{ focus, blur }"
                            @on-open="focus"
                            @on-close="blur"
                            :config="{ allowInput: true }"
                            class="form-control datepicker"
                            v-model="modal.child.birth_date"
                          >
                          </flat-picker>
                        </base-input>
                      </div>
                    </div>
                  </div>
                </div>
                <template slot="footer">
                  <base-button type="secondary" @click="modal.show = false"
                    >Annuler</base-button
                  >
                  <base-button type="primary" @click="submitModal">
                    <template v-if="modal.action == 'add'">Ajouter</template>
                    <template v-else-if="modal.action == 'update'"
                      >Modifier</template
                    >
                    <template v-else-if="modal.action == 'delete'"
                      >Retirer</template
                    >
                  </base-button>
                </template>
              </modal>
              <modal :show.sync="picture_modal.show">
                <template slot="header">
                  <h5>Modifier ma photo</h5>
                </template>
                <div>
                  <div class="row justify-content-center text-left">
                    <div class="col-lg-9">
                      <base-input
                        v-model="modal.child.first_name"
                        label="Prénom"
                        placeholder="Prénom"
                        required
                        :error="modal.errors.first_name"
                      ></base-input>
                      <base-input
                        v-model="modal.child.last_name"
                        label="Nom"
                        placeholder="Nom"
                        required
                        :error="modal.errors.last_name"
                      ></base-input>
                      <base-input
                        label="Sexe"
                        placeholder="Sexe"
                        required
                        :error="modal.errors.gender"
                        ><select
                          v-model="modal.child.gender"
                          class="form-control"
                        >
                          <option value="male">Garçon</option>
                          <option value="female">Fille</option>
                        </select></base-input
                      >
                      <base-input
                        label="Date de naissance"
                        required
                        :error="modal.errors.birth_date"
                      >
                        <flat-picker
                          slot-scope="{ focus, blur }"
                          @on-open="focus"
                          @on-close="blur"
                          :config="{ allowInput: true }"
                          class="form-control datepicker"
                          v-model="modal.child.birth_date"
                        >
                        </flat-picker>
                      </base-input>
                    </div>
                  </div>
                </div>
                <template slot="footer">
                  <base-button
                    type="secondary"
                    @click="picture_modal.show = false"
                    >Annuler</base-button
                  >
                  <base-button type="primary" @click="submitPictureModal"
                    >Modifier</base-button
                  >
                </template>
              </modal>
            </div>
          </div>
        </card>
      </div>
    </section>
  </div>
</template>
<script>
import Modal from "@/components/Modal.vue";
import BaseButton from "@/components/BaseButton";
import BaseInput from "@/components/BaseInput";
import flatPicker from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import * as types from "../store/mutation-types";
export default {
  components: {
    Modal,
    BaseButton,
    BaseInput,
    flatPicker,
  },
  title: "Mes enfants",
  data() {
    return {
      child_statuses: {
        "registered": "Enregistrer",
        "in_validation": "Validation"
      },
      userData: "",
      modal: { show: false, child: {}, errors: {} },
      picture_modal: { show: false },
    };
  },
  mounted() {
    this.$store.dispatch(types.GET_USER, this.currentUserId);
    this.$store.dispatch(types.GET_CHILDREN);
  },
  methods: {
    addChildForm() {
      this.modal.show = true;
      this.modal.child = {};
      this.modal.action = "add";
    },
    editChildForm(child_id) {
      this.modal.show = true;
      this.modal.child = this.children.find((c) => c.id == child_id);
      this.modal.action = "update";
    },
    removeChildForm(child_id) {
      this.modal.show = true;
      this.modal.child = this.children.find((c) => c.id == child_id);
      this.modal.action = "delete";
    },
    pictureModal() {
      this.picture_modal.show = true;
    },
    submitPictureModal() {},
    submitModal() {
      if (this.modal.action == "delete") {
        this.$store
          .dispatch(types.DELETE_CHILD, this.modal.child.id)
          .then(() => {
            this.modal = {
              show: false,
              child: {},
              errors: {},
            };
          });
        return;
      }
      let has_error = false;
      if (!this.modal.child.first_name) {
        this.modal.errors.first_name = "Champs obligatoire";
        has_error = true;
      }
      if (!this.modal.child.last_name) {
        this.modal.errors.last_name = "Champs obligatoire";
        has_error = true;
      }
      if (!this.modal.child.gender) {
        this.modal.errors.gender = "Champs obligatoire";
        has_error = true;
      }
      if (!this.modal.child.birth_date) {
        this.modal.errors.birthdate = "Champs obligatoire";
        has_error = true;
      }
      if (has_error) {
        return;
      }
      if (this.modal.action == "add") {
        this.$store.dispatch(types.CREATE_CHILD, this.modal.child).then(() => {
          this.modal = {
            show: false,
            child: {},
            errors: {},
          };
        });
      } else if (this.modal.action == "update") {
        this.$store.dispatch(types.UPDATE_CHILD, this.modal.child).then(() => {
          this.modal = {
            show: false,
            child: {},
            errors: {},
          };
        });
      }
    },
  },
  computed: {
    currentUserId() {
      return this.$store.getters.getCurrentUserId;
    },
    currentUser() {
      return this.$store.getters.getUser(this.currentUserId);
    },
    children() {
      return this.$store.getters.getChildren;
    },
    numberOfChildren() {
      return this.children.length;
    },
  },
};
</script>
<style>
</style>
