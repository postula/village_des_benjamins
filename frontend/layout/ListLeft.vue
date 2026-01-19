<template>
  <section class="section section section-shaped my-0" :id="section.key">
  <div class="inversed_skew shape" :style="cssVars">
    <WhiteDot top="10%" left="5%" :opacity=".05"/>
    <WhiteDot top="15%" left="10%" :opacity=".10"/>
    <WhiteDot top="90%" left="15%" :opacity=".05"/>
    <WhiteDot top="95%" left="20%" :opacity=".10"/>
    <WhiteDot top="10%" left="95%" :opacity=".05"/>
    <WhiteDot top="56%" left="45%" :opacity=".10"/>
    <WhiteDot top="58%" left="56%" :opacity=".05"/>
  </div>
  <div class="container py-0" :id="section.key">
    <div class="row row-grid align-items-center">
      <div class="col-md-6 order-lg-2 ml-lg-auto">
        <div class="position-relative pl-md-5">
          <img :src="section.photo" class="img-center img-fluid">
        </div>
      </div>
      <div class="d-flex px-3">
        <div>
          <icon name="ni ni-building" size="lg" class="bg-gradient-white" color="primary" shadow
                rounded></icon>
        </div>
        <div class="pl-4">
          <h2 class="display-3">{{section.name}}</h2>
          <p class="text-white" v-html="section.description"></p>
        </div>
      </div>

      <div class="col-lg-6 order-lg-1">
        <card shadow class="shadow-lg--hover mt-5" v-for="item in ordered_items" :key="item.id">
          <div class="d-flex px-3">
            <div>
              <icon v-show="item.icon" :name="`fa fa-${item.icon}`" gradient="success" color="white"
                    shadow
                    rounded></icon>
            </div>
            <div class="pl-4">
              <h5 class="title text-success">{{ item.name }}</h5>
              <p v-html="item.description"></p>
              <base-button v-if="item.show_more_button" type="primary" @click="showMore(item.id, $event)">{{item.show_more_button}}</base-button>
              <modal v-if="item.show_more_button && (item.show_more_content || item.planning_entries)"
                     @close="hideMore"
                     :show="show_more_item === item.id"
                     modal-classes="modal-lg">
                <template slot="header">
                  <h5 class="modal-title" >{{item.show_more_button}}</h5>
                </template>
                <div>
                  <!-- Show introduction/description text if present -->
                  <div v-if="item.show_more_content" v-html="item.show_more_content" class="mb-4"></div>

                  <!-- Show planning table if entries exist -->
                  <div v-if="item.planning_entries && item.planning_entries.length > 0" class="planning-container">
                    <h5 class="mb-3">Planning des activités</h5>
                    <div class="table-responsive">
                      <table class="table table-striped table-hover">
                        <thead class="thead-light">
                          <tr>
                            <th class="planning-date">Date</th>
                            <th class="planning-educator">Animateur</th>
                            <th class="planning-section">Groupe</th>
                            <th class="planning-activity">Activité</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="entry in getFutureEntries(item.planning_entries)" :key="entry.id">
                            <td data-label="Date" class="planning-date">{{ entry.date }}</td>
                            <td data-label="Animateur" class="planning-educator">{{ entry.educator_name }}</td>
                            <td data-label="Groupe" class="planning-section">{{ entry.section_name }}</td>
                            <td data-label="Activité" class="planning-activity">{{ entry.description }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </modal>
            </div>
          </div>
        </card>
      </div>
    </div>
  </div>
</section>
</template>

<script>
import WhiteDot from "../components/WhiteDot";
import Modal from "../components/Modal";

const order_sort = (a, b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0);

export default {
  name: "ListLeft",
  components: {
    WhiteDot,
    Modal,
  },
  data() {
    return {
      show_more_item: null,
    };
  },
  methods: {
    showMore: function (contentId, evt) {
      evt.preventDefault();
      this.show_more_item = contentId;
    },
    hideMore: function (contentId, evt) {
      this.show_more_item = null;
    },
    getFutureEntries: function (entries) {
      if (!entries) return [];
      const today = new Date();
      today.setHours(0, 0, 0, 0);

      return entries.filter(entry => {
        // Parse date in dd/mm/yyyy format
        const [day, month, year] = entry.date.split('/');
        const entryDate = new Date(year, month - 1, day);
        return entryDate >= today;
      });
    },
  },
  computed: {
    ordered_items() {
      return this.items.sort(order_sort);
    },
    cssVars() {
      return {
        "--background": this.section.background,
      };
    },
  },
  props: {
    section: Object,
    items: Array,
  }
}
</script>

<style scoped>

.inversed_skew {
  transform: skewY(-8deg);
  transform-origin: -180px;
      position: absolute;
    top: 0;
    z-index: -1;
    width: 100%;
    height: 100%;
  background: var(--background);
}
/* Planning table styles */
.planning-container {
  max-height: 70vh;
  overflow-y: auto;
}

.planning-container .table {
  margin-bottom: 0;
}

.planning-date {
  width: 15%;
  white-space: nowrap;
}

.planning-educator {
  width: 20%;
}

.planning-section {
  width: 20%;
}

.planning-activity {
  width: 45%;
}

/* Mobile responsive - stack table as cards */
@media (max-width: 768px) {
  .planning-container .table thead {
    display: none;
  }

  .planning-container .table,
  .planning-container .table tbody,
  .planning-container .table tr,
  .planning-container .table td {
    display: block;
    width: 100%;
  }

  .planning-container .table tr {
    margin-bottom: 1rem;
    border: 1px solid #dee2e6;
    border-radius: 0.375rem;
    padding: 0.75rem;
    background: #fff;
  }

  .planning-container .table td {
    text-align: right;
    padding: 0.5rem 0;
    border: none;
    position: relative;
    padding-left: 50%;
  }

  .planning-container .table td::before {
    content: attr(data-label);
    position: absolute;
    left: 0;
    width: 45%;
    padding-right: 10px;
    font-weight: bold;
    text-align: left;
  }
}
</style>
