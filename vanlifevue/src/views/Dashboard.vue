<template>
  <v-app>
    <v-card>
      <v-card-title primary-title>
        <div>
          <h3 class="headline mb-0">Dashboard</h3>
        </div>
      </v-card-title>
      <span class="ml-4 display-4">{{ Time }}</span>
      <weather />
    </v-card>
  </v-app>
</template>

<script>
import weather from "@/components/weather";

export default {
  name: "Dashboard",

  components: {
    weather
  },
  data() {
    return {
      Time: ""
    }
  },
  mounted() {
    setInterval(() => {
      this.Time = this.GetTime()
    }, 10);
  },
  methods: {
    GetTime() {
      let today = new Date();
      let h = today.getHours();
      let m = today.getMinutes();
      let s = today.getSeconds();
      h = this.checkTime(h);
      m = this.checkTime(m);
      s = this.checkTime(s);
      return `${h}:${m}:${s}`;
    },
    checkTime(i) {
      if (i < 10) {
        i = "0" + i;
      }
      return i;
    }
  }
};
</script>
