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
        <card shadow class="card-profile mt--300">
          <h5 class="card-title">Réservations ouvertes</h5>
          <div class="px-4">
            <div class="text-center">
              <div class="row justify-content-center">
                <div class="col-lg-12">
                  <div class="list-group">
                    <!-- <h5 class="col-xl-12 text-left">{{ holiday.name }}</h5>
                    <div class="col-sm-12 col-md-6">
                      {{ holiday.start_date }} - {{ holiday.end_date }}
                    </div>
                    <div class="col-sm-12 col-md-6">
                      {{ holiday.price }}€ / jour
                    </div> -->
                    <div
                      v-for="holiday in holidays"
                      :key="holiday.id"
                      class="list-group-item list-group-item-action flex-column align-items-start"
                    >
                      <div
                        class="d-flex w-100 justify-content-center justify-content-md-between flex-wrap"
                      >
                        <h5 class="mb-1">
                          {{ holiday.name }}
                        </h5>
                        <div
                          class="d-flex justify-content-between flex-column align-items-center align-items-md-end"
                        >
                          <span>{{ holiday.price }}€ / jour</span>
                          <div class="">
                            <i class="fa fa-calendar" />
                            {{
                              new Date(holiday.start_date).toLocaleDateString(
                                "fr-BE"
                              )
                            }}
                            -
                            {{
                              new Date(holiday.end_date).toLocaleDateString(
                                "fr-BE"
                              )
                            }}
                          </div>
                        </div>
                      </div>
                      <div class="mt-2">
                        <tabs
                          type="info"
                          fill
                          centered
                          class="flex-column flex-md-row text-left"
                        >
                          <card shadow>
                            <tab-pane>
                              <span slot="title">Informations Générales</span>
                              <span v-html="holiday.description"></span>
                            </tab-pane>
                            <tab-pane
                              v-for="section in holiday.sections"
                              :key="section.id"
                            >
                              <span slot="title">
                                {{ section.section_name }}
                              </span>

                              <div class="mt-1" v-html="section.description">
                              </div>
                              <div v-if="section.outings.length > 0">
                                <h4 class="mt-2">Sorties</h4>
                                <div class="list-group">
                                  <div
                                    v-for="outing in section.outings"
                                    :key="outing.id"
                                    class="list-group-item list-group-item-action flex-column align-items-start"
                                  >
                                    <div
                                      class="d-flex w-100 justify-content-center justify-content-md-between flex-wrap"
                                    >
                                      <h5 class="mb-1">
                                        {{ outing.name }}
                                      </h5>
                                      <div
                                        class="d-flex justify-content-between flex-column align-items-center align-items-md-end"
                                      >
                                        <span
                                          ><i class="fa fa-calendar mr-1" />{{
                                            formatDate(outing.date)
                                          }}</span
                                        ><span
                                          ><i class="fa fa-hourglass mr-1" />{{
                                            formatTime(outing.departure_time)
                                          }}-{{
                                            formatTime(outing.arrival_time)
                                          }}</span
                                        >
                                        <span>{{ outing.price }} €</span>
                                        <span>{{ outing.transport }}</span>
                                      </div>
                                    </div>
                                    <div>
                                      <p class="description" v-html="outing.description">
                                      </p>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </tab-pane>
                          </card>
                        </tabs>
                      </div>
                      <div class="mt-1">
                        <base-button
                          type="success"
                          icon="fa fa-plus"
                          @click="makeReservation(holiday.id)"
                          :disabled="
                            children.filter(
                              (c) => !c.holidays_booked.includes(holiday.id)
                            ).length == 0
                          "
                          >Réserver</base-button
                        >
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <modal
                :show.sync="reservation_modal.show"
                modal-classes="modal-dialog-centered modal-lg"
              >
                <template slot="header">
                  <h5>
                    {{
                      reservation_modal.action == "add" ? "Ajouter" : "Modifier"
                    }}
                    une réservation pour {{ reservation_modal.holiday.name }}
                  </h5>
                </template>
                <div>
                  <div class="row justify-content-center text-left">
                    <div class="col-lg-9">
                      <base-input
                        label="Enfant"
                        required
                        :error="reservation_modal.errors.child_id"
                        ><select
                          v-model="reservation_modal.child_id"
                          @change="setChildId"
                          class="form-control"
                        >
                          <option
                            v-for="child in reservation_modal.children"
                            :key="child.id"
                            :value="child.id"
                          >
                            {{ child.first_name }} {{ child.last_name }}
                          </option>
                        </select></base-input
                      >
                      <base-input
                        label="Groupe"
                        readonly
                        :value="reservationModalSection.section_name"
                      ></base-input>
                      <base-input
                        label="Dates"
                        required
                        :error="reservation_modal.errors.dates"
                      >
                        <flat-picker
                          slot-scope="{ focus, blur }"
                          @on-open="focus"
                          @on-close="blur"
                          :disabled="!reservation_modal.child_id"
                          :config="reservation_modal.dp_config"
                          @on-day-create="onDayCreate"
                          :events="['onChange', 'onDayCreate']"
                          class="form-control datepicker"
                          v-model="reservation_modal.dates"
                        >
                        </flat-picker>
                      </base-input>
                      <base-input label="Prix" readonly>
                        <table class="table table-borderless">
                          <tr>
                            <td>Journée</td>
                            <td>
                              {{ numDayChoosen }}
                            </td>
                            <td>x</td>
                            <td>{{ reservation_modal.holiday.price }}</td>
                            <td>=</td>
                            <td>
                              {{
                                numDayChoosen * reservation_modal.holiday.price
                              }}
                            </td>
                          </tr>
                          <tr
                            v-for="outing in currentSection.outings"
                            :key="outing.id"
                          >
                            <td>Sortie {{ outing.name }}</td>
                            <td>{{ outingsBooked[outing.id] ? 1 : 0 }}</td>
                            <td>x</td>
                            <td>{{ outing.price }}</td>
                            <td>=</td>
                            <td>
                              {{
                                (outingsBooked[outing.id] ? 1 : 0) *
                                outing.price
                              }}
                            </td>
                          </tr>
                          <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td><b>Total</b></td>
                            <td>
                              {{ bookingPrice }}
                            </td>
                          </tr>
                        </table>
                      </base-input>
                    </div>
                  </div>
                </div>
                <template slot="footer">
                  <base-button
                    type="secondary"
                    @click="reservation_modal.show = false"
                    >Annuler</base-button
                  >
                  <base-button type="primary" @click="submitReservationModal">{{
                    reservation_modal.action == "add" ? "Réserver" : "Modifier"
                  }}</base-button>
                </template>
              </modal>
            </div>
          </div>
          <h5 class="card-title border-top mt-5 py-5">Mes Réservations</h5>
          <div class="px-4">
            <div class="text-center">
              <div class="row justify-content-center">
                <div class="col-lg-12">
                  <div class="list-group">
                    <div
                      v-for="registration in registrations"
                      :key="registration.id"
                      class="list-group-item list-group-item-action flex-column align-items-start"
                    >
                      <div
                        class="d-flex w-100 justify-content-center justify-content-md-between flex-wrap"
                      >
                        <h5 class="mb-1">
                          {{
                            (
                              holidays.find(
                                (h) => h.id == registration.holiday
                              ) || {}
                            ).name
                          }}
                        </h5>
                        <div
                          class="d-flex justify-content-between flex-column align-items-center align-items-md-end"
                        >
                          <span>{{ registration.cost }}€</span>
                          <div>
                            {{ registration_statuses[registration.status] }}
                            <i
                              :class="`fa fa-circle text-${registration.status_type}`"
                            />
                          </div>
                        </div>
                      </div>
                      <div
                        class="d-flex w-100 justify-content-center justify-content-md-between flex-wrap"
                      >
                        <h6 class="mb-1">
                          {{
                            getChildName(
                              children.find((c) => c.id == registration.child)
                            )
                          }}
                        </h6>
                        <div>
                          {{
                            registration.dates
                              .map((d) =>
                                new Date(d).toLocaleDateString("fr-BE")
                              )
                              .join(", ")
                          }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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
import Tabs from "@/components/Tabs/Tabs";
import TabPane from "@/components/Tabs/TabPane";
import flatPicker from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import * as types from "../store/mutation-types";
import { DateTime, Settings } from "luxon";
export default {
  components: {
    Modal,
    BaseButton,
    BaseInput,
    Tabs,
    TabPane,
    flatPicker,
  },
  data() {
    return {
      // userData: "",
      reservationModalSection: {},
      reservation_modal: {
        show: false,
        dates: "",
        holiday: {},
        child_id: undefined,
        errors: {},
        chidren: [],
        action: null,
        dp_config: {
          allowInput: true,
          mode: "multiple",
          inline: true,
          locale: {
            firstDayOfWeek: 1,
          },
        },
      },
      registration_statuses: {
        pending: "impayée",
        paid: "payée",
        cancelled: "annulée",
      },
      // modal: { show: false, child: {}, errors: {} },
      // picture_modal: { show: false },
    };
  },
  mounted() {
    Settings.defaultLocale = "fr";
    this.$store.dispatch(types.GET_HOLIDAYS);
    this.$store.dispatch(types.GET_CHILDREN);
    this.$store.dispatch(types.GET_REGISTRATIONS);
  },
  methods: {
    log(item) {
      console.log(item);
    },
    formatDate(d) {
      return DateTime.fromISO(d).toLocaleString(DateTime.DATE_FULL);
    },
    formatTime(t) {
      return DateTime.fromISO(t).toLocaleString(DateTime.TIME_24_SIMPLE);
    },
    onDayCreate(dObj, dStr, fp, dayElem) {
      const d = DateTime.fromJSDate(dayElem.dateObj);
      if (this.currentSection) {
        const outings = this.currentSection.outings;
        if (outings && outings.length != 0) {
          for (const outing of outings) {
            const c_d = DateTime.fromISO(outing.date);
            if (c_d.hasSame(d, "day")) {
              dayElem.innerHTML +=
                "<span class='badge badge-warning'><i class='fa fa-star' /></span>";
            }
          }
        }
      }
    },
    getChildName(c) {
      if (!c) return;
      return `${c.first_name} ${c.last_name}`;
    },
    setChildId() {
      const child_id = this.reservation_modal.child_id;
      this.reservation_modal.child_id = child_id;
      const child = this.children.find((c) => c.id == child_id);
      if (!child) return;
      this.reservationModalSection =
        this.reservation_modal.holiday.sections.find(
          (s) => s.section_name == child.section
        ) || {};
      const dates = [];
      for (const date in this.reservationModalSection.capacities) {
        const capacity = this.reservationModalSection.capacities[date];
        if (capacity <= 0) {
          dates.push(date);
        }
      }
      this.$set(this.reservation_modal.dp_config, "disable", dates);
    },
    makeReservation(holiday_id) {
      this.reservation_modal = Object.assign(this.reservation_modal, {
        show: true,
        dates: "",
        holiday: this.holidays.find((h) => h.id == holiday_id),
        child_id: undefined,
        errors: {},
        children: this.children.filter(
          (c) => !c.holidays_booked.includes(holiday_id)
        ),
        action: "add",
      });
      this.$set(
        this.reservation_modal.dp_config,
        "minDate",
        this.reservation_modal.holiday.start_date
      );
      this.$set(
        this.reservation_modal.dp_config,
        "maxDate",
        this.reservation_modal.holiday.end_date
      );
    },
    submitReservationModal() {
      let has_error = false;
      if (!this.reservation_modal.child_id) {
        this.reservation_modal.errors.child_id = "Champs obligatoire";
        has_error = true;
      }
      if (
        !this.reservation_modal.dates ||
        this.reservation_modal.dates.split(",").length == 0
      ) {
        this.reservation_modal.errors.dates = "Champs obligatoire";
        has_error = true;
      }
      if (has_error) {
        return;
      }
      this.$store
        .dispatch(types.CREATE_REGISTRATION, {
          child: this.reservation_modal.child_id,
          holiday: this.reservation_modal.holiday.id,
          dates: this.reservation_modal.dates.split(", "),
          section: this.reservationModalSection.section_id,
        })
        .then(() => {
          this.reservation_modal.show = false;
        });
    },
  },
  computed: {
    currentSection() {
      if (!this.reservation_modal.show) return {};
      if (!this.reservation_modal.child_id) return {};
      const child = this.children.find(
        (c) => c.id == this.reservation_modal.child_id
      );
      const section_name = child.section;
      return this.reservation_modal.holiday.sections.find(
        (c) => c.section_name == section_name
      );
    },
    dayChoosen() {
      if (!this.reservation_modal.show || !this.reservation_modal.dates)
        return [];
      return this.reservation_modal.dates.split(", ");
    },
    numDayChoosen() {
      return this.dayChoosen.length;
    },
    outingsBooked() {
      const section = this.currentSection;
      if (!section.outings) return {};
      const dayChoosen = this.dayChoosen.map((d) => DateTime.fromISO(d));
      const out = {};
      for (const outing of section.outings) {
        if (this.dayChoosen.includes(outing.date)) {
          out[outing.id] = true;
        } else {
          out[outing.id] = false;
        }
      }
      return out;
    },
    bookingPrice() {
      const section = this.currentSection;
      if (!section.outings) return 0;
      let out = 0;
      out += this.dayChoosen.length * this.reservation_modal.holiday.price;
      for (const outing of section.outings) {
        if (this.dayChoosen.includes(outing.date)) {
          out += Number(outing.price);
        }
      }
      return out;
    },
    holidays() {
      return this.$store.getters.getHolidays.filter((h) => h.registration_open);
    },
    children() {
      return this.$store.getters.getChildren.filter(c => c.status === "registered");
    },
    registrations() {
      return this.$store.getters.getRegistrations;
    },
  },
};
</script>
<style>
</style>
