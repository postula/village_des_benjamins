<template>
  <div class="profile-page">
    <Skew :dots="7" />
    <section class="section section-skew">
      <div class="container">
        <card shadow class="card-profile mt--300" body-classes="px-1 px-md-4">
          <h5 slot="header">Réservations ouvertes</h5>
          <div class="text-center">
            <div class="row justify-content-center">
              <div class="col-lg-12">
                <div class="list-group">
                  <div
                      v-for="holiday in holidays"
                      :key="holiday.id"
                      class="list-group-item list-group-item-action flex-column align-items-start px-1"
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
                        <span v-if="holiday.registration_open">{{ holiday.price }}€ / jour</span>
                        <div class="">
                          <i class="fa fa-calendar"/>
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
                            <div class="mt-1" v-html="section.description" />
                            <HolidaySection title="Programme">
                              <ProgramCard
                                    v-for="activity in section.activities"
                                    :key="activity.id"
                                    :start_date="activity.start_date"
                                    :end_date="activity.end_date"
                                    :educators="activity.educators"
                                    :theme="activity.theme"
                                    :description="activity.description"
                                    :bricolage="activity.bricolage"
                                    :food="activity.food"
                                    :game="activity.game"
                                    :other="activity.other"
                                />
                            </HolidaySection>
                            <HolidaySection
                                v-if="section.outings.length > 0"
                                title="Sorties et Activités Payantes"
                            >
                              <Outing
                                v-for="outing in section.outings"
                                :key="outing.id"
                                :name="outing.name"
                                :start_date="outing.start_date"
                                :end_date="outing.end_date"
                                :arrival_time="outing.arrival_time"
                                :departure_time="outing.departure_time"
                                :price="outing.price"
                                :transport="outing.transport"
                                :description="outing.description"
                              />
                            </HolidaySection>
                          </tab-pane>
                        </card>
                      </tabs>
                    </div>
                    <div class="mt-1" v-if="holiday.registration_open || is_staff">
                      <base-button
                          type="success"
                          icon="fa fa-plus"
                          @click="makeReservation(holiday.id)"
                          :disabled="
                            children.filter(
                              (c) => !c.holidays_booked.includes(holiday.id)
                            ).length == 0
                          "
                      >Réserver
                      </base-button
                      >
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </card>
        <card shadow class="mt-5" body-classes="px-1 px-md-4">
          <h5 slot="header">Mes Réservations</h5>
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
        <modal
          :show.sync="reservation_modal.show"
          modal-classes="modal-dialog-centered modal-lg"
        >
          <h5 slot="header"> Ajouter une réservation pour {{ reservation_modal.holiday.name }}</h5>
          <div>
            <div v-if="capacityLoading">
              <div id="loading"/>
            </div>
            <div class="row justify-content-center text-left" v-else>
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
                      @on-open="onOpen"
                      @on-close="blur"
                      :disabled="!reservation_modal.child_id"
                      :config="reservation_modal.dp_config"
                      @on-day-create="onDayCreate"
                      :events="['onChange', 'onDayCreate', 'onOpen']"
                      class="form-control datepicker"
                      :value="reservation_modal.dates"
                      @on-change="dateChanged"
                  >
                  </flat-picker>
                </base-input>
                <base-input
                    label="Problème de santé / Allergies"
                >
                  <textarea
                      class="form-control"
                      rows="4"
                      placeholder="Si votre enfant souffre d'allergies ou d'un problème santé, veuillez le noter ici"
                      v-model="reservation_modal.notes"
                  ></textarea>
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
                      <td>
                        <div class="d-flex flex-column">
                          <span>Sortie / Activité spéciale</span>
                          <span class="text-bold">{{ outing.name }}</span>
                          <span>{{ formatDate(outing.date) }}</span>
                        </div>
                      </td>
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
            >Annuler
            </base-button
            >
            <base-button type="primary" @click="submitReservationModal">{{
                reservation_modal.action == "add" ? "Réserver" : "Modifier"
              }}
            </base-button>
          </template>
        </modal>
      </div>
    </section>
  </div>
</template>
<script>
import flatPicker from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";

import {DateTime, Interval, Settings} from "luxon";

import Modal from "@/components/Modal.vue";
import BaseButton from "@/components/BaseButton";
import BaseInput from "@/components/BaseInput";
import Tabs from "@/components/Tabs/Tabs";
import TabPane from "@/components/Tabs/TabPane";
import ProgramCard from "@/components/ProgramCard";
import HolidaySection from "@/components/HolidaySection";
import Outing from "@/components/Outing";
import Skew from "@/components/Skew";

import * as types from "@/store/mutation-types";
import {getChildSection} from "../store";

export default {
  components: {
    Modal,
    BaseButton,
    BaseInput,
    Tabs,
    TabPane,
    flatPicker,
    HolidaySection,
    ProgramCard,
    Outing,
    Skew,
  },
  title: "Réservation",
  data() {
    return {
      // userData: "",
      reservationModalSection: {},
      reservation_modal: {
        show: false,
        dates: null,
        notes: "",
        holiday: {},
        child_id: undefined,
        errors: {},
        chidren: [],
        action: null,
        dp_config: {
          allowInput: true,
          mode: "multiple",
          inline: false,
          locale: {
            firstDayOfWeek: 1,
          },
        },
      },
      currentChildSection: "",
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
    dateChanged(selectedDates, dateStr, instance) {
      let current_dates = [];
      if (this.reservation_modal.dates) {
        current_dates = this.reservation_modal.dates.split(", ");
      }
      const new_dates = dateStr.split(", ");
      let date;
      let action;
      if (!dateStr || current_dates.length > new_dates.length) {
        if (current_dates.length === 1) {
          date = current_dates[0];
        } else {
          date = current_dates.filter(f => !new_dates.includes(f))[0];
        }
        action = "remove";
      } else {
        date = new_dates.filter(f => !current_dates.includes(f))[0];
        action = "add";
      }
      if (!date) {
        return;
      }
      const min_date = instance.parseDate(this.reservation_modal.holiday.start_date, "Y-m-d");
      const max_date = instance.parseDate(this.reservation_modal.holiday.end_date, "Y-m-d");
      const additional_dates = [date];
      if (!this.reservation_modal.holiday.book_by_day) {
        const parsed_date = instance.parseDate(date, "Y-m-d");
        let weekday = parsed_date.getDay();
        while (weekday > 1) {
          const cand_date = new Date(parsed_date);
          cand_date.setDate(cand_date.getDate() - (parsed_date.getDay() - weekday + 1));
          if (cand_date >= min_date) {
            const date_str = instance.formatDate(cand_date, "Y-m-d");
            if (!this.reservation_modal.dp_config.disable.includes(date_str)) {
              additional_dates.push(instance.formatDate(cand_date, "Y-m-d"));
            }
            weekday -= 1;
          } else {
            weekday = 0;
          }
        }
        weekday = parsed_date.getDay();
        while (weekday < 5) {
          const cand_date = new Date(parsed_date);
          cand_date.setDate(cand_date.getDate() + (weekday - parsed_date.getDay() + 1));
          if (cand_date <= max_date) {
            const date_str = instance.formatDate(cand_date, "Y-m-d");
            if (!this.reservation_modal.dp_config.disable.includes(date_str)) {
              additional_dates.push(instance.formatDate(cand_date, "Y-m-d"));
            }
            weekday += 1;
          } else {
            weekday = 5;
          }
        }
      }
      if (action === "add") {
        current_dates = current_dates.concat(additional_dates);
      } else {
        current_dates = current_dates.filter(d => !additional_dates.includes(d));
      }
      if (current_dates.length > 0) {
        this.reservation_modal.dates = current_dates.join(", ");
      } else {
        this.reservation_modal.dates = null;
        instance.jumpToDate(min_date);
      }
    },
    log(item) {
      //console.log(item);
    },
    formatDate(d) {
      return DateTime.fromISO(d).toLocaleString(DateTime.DATE_FULL);
    },
    formatTime(t) {
      return DateTime.fromISO(t).toLocaleString(DateTime.TIME_24_SIMPLE);
    },
    onOpen(selectedDates, dateStr, instance) {
      instance.redraw();
    },
    onDayCreate(dObj, dStr, fp, dayElem) {
      const d = DateTime.fromJSDate(dayElem.dateObj);
      // if (this.reservationModalSection && this.reservationModalSection.capacities) {
      //   console.log(dayElem.dateObj.toDateString(DateTime.DATE_FULL))
      //   const capacity = this.reservationModalSection.capacities[dStr];
      //   if (capacity <= 0) {
      //     console.log(dayElem);
      //   }
      // }
      if (this.currentSection) {
        const outings = this.currentSection.outings;
        if (outings && outings.length != 0) {
          for (const outing of outings) {
            let out = false;
            const s_o_d = DateTime.fromISO(outing.start_date);
            if (!!outing.end_date) {
              // interval
              const e_o_d = DateTime.fromISO(outing.end_date).plus({days: 1});
              let interval = Interval.fromDateTimes(s_o_d, e_o_d);
              if (interval.contains(d)) {
                out = true;
              }
            } else {
              if (s_o_d.hasSame(d, "day")) {
                out = true;
              }
            }
            if (out) {
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
    async setChildId() {
      const child_id = this.reservation_modal.child_id;
      const child = this.children.find((c) => c.id === child_id);
      if (!child) {
        this.$set(
          this.reservation_modal.dp_config,
          "inline",
          false
        );
        return;
      }
      const { section_name } = await getChildSection({
        holiday_id: this.reservation_modal.holiday.id,
        child_id
      });
      this.reservation_modal.child_id = child_id;
      this.currentChildSection = section_name;
      this.reservationModalSection =
        this.reservation_modal.holiday.sections.find(
          (s) => s.section_name === this.currentChildSection
        ) || {};
      const dates = [];
      const start = new Date(this.reservation_modal.holiday.start_date);
      const end = new Date(this.reservation_modal.holiday.end_date);
      let loop = new Date(start);
      while(loop <= end){
        let loop_str = `${loop.getFullYear()}-${String(loop.getMonth() + 1).padStart(2, "0")}-${String(loop.getDate()).padStart(2, "0")}`;
        let newDate = loop.setDate(loop.getDate() + 1);
        const capacity = this.reservationModalSection.capacities && this.reservationModalSection.capacities[loop_str];
        if (!capacity) {
          dates.push(loop_str);
        }
        loop = new Date(newDate);
      }
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
      this.$set(this.reservation_modal.dp_config, "disable", dates);
    },
    makeReservation(holiday_id) {
      this.$store.dispatch(types.GET_HOLIDAYS_SECTION_CAPACITY, {
        holiday_id: holiday_id
      })
      this.reservation_modal = Object.assign(this.reservation_modal, {
        show: true,
        dates: "",
        holiday: this.holidays.find((h) => h.id === holiday_id),
        child_id: undefined,
        errors: {},
        children: this.children.filter(
          (c) => !c.holidays_booked.includes(holiday_id)
        ),
        action: "add",
      });
    },
    submitReservationModal() {
      let has_error = false;
      if (!this.reservation_modal.child_id) {
        this.reservation_modal.errors.child_id = "Champs obligatoire";
        has_error = true;
      }
      if (
        !this.reservation_modal.dates ||
        this.reservation_modal.dates.split(",").length === 0
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
          notes: this.reservation_modal.notes,
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
      if (!this.currentChildSection) return {};
      return this.reservation_modal.holiday.sections.find(
        (c) => c.section_name === this.currentChildSection
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
      const out = {};
      const section = this.currentSection;
      if (!section.outings) return out;
      for (const outing of section.outings) {
        let booked = false;
        const s_o_d = DateTime.fromISO(outing.start_date);
        if (!!outing.end_date) {
          // interval
          const e_o_d = DateTime.fromISO(outing.end_date).plus({days: 1});
          let interval = Interval.fromDateTimes(s_o_d, e_o_d);
          for (const d_s of this.dayChoosen) {
            const d = DateTime.fromFormat(d_s, "yyyy-MM-dd");
            if (interval.contains(d)) {
              booked = true;
              break;
            }
          }
        } else {
          for (const d_s of this.dayChoosen) {
            const d = DateTime.fromFormat(d_s, "yyyy-MM-dd");
            if (s_o_d.hasSame(d, "day")) {
              booked = true;
              break;
            }
          }
        }
        out[outing.id] = booked;
      }
      return out;
    },
    bookingPrice() {
      const section = this.currentSection;
      if (!section.outings) return 0;
      let outings_booked = this.outingsBooked;
      let out = 0;
      out += this.dayChoosen.length * this.reservation_modal.holiday.price;
      for (const outing of section.outings) {
        if (outings_booked(outing.id)) {
          out += Number(outing.price);
        }
      }
      return out.toFixed(2);
    },
    holidays() {
      return this.$store.getters.getHolidays;
    },
    children() {
      return this.$store.getters.getChildren.filter(c => c.status === "registered");
    },
    registrations() {
      return this.$store.getters.getRegistrations;
    },
    capacityLoading() {
      return this.$store.getters.getCapacityLoading;
    },
    is_staff() {
      return this.$store.getters.IsStaff;
    }
  },
};
</script>
<style scoped>

#loading {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255,255,255,.3);
  border-radius: 50%;
  border-top-color: black;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { -webkit-transform: rotate(360deg); }
}
@-webkit-keyframes spin {
  to { -webkit-transform: rotate(360deg); }
}
</style>
