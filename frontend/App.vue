<template>
    <div id="app">
        <router-view name="header"></router-view>
        <main>
            <fade-transition origin="center" mode="out-in" :duration="250">
                <router-view/>
            </fade-transition>
        </main>
        <router-view name="footer"></router-view>
        <cookie-law
            @accept="acceptCookie"
            buttonText="J'ai compris!"
            message="Ce site Web utilise des cookies pour vous garantir la meilleure expérience possible sur notre site."
        >
        </cookie-law>
    </div>
</template>
<script>
import { FadeTransition } from "vue2-transitions";
import CookieLaw from 'vue-cookie-law';
import { bootstrap } from 'vue-gtag'

export default {
  components: {
    FadeTransition,
    CookieLaw,
  },
  methods: {
    acceptCookie() {
      bootstrap()
    },
    refuseCookie() {

    }
  }
};
</script>
