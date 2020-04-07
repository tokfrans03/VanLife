<template>
  <v-card class="my-2">
    <v-card-title>{{ Title }}</v-card-title>
    <v-card-text>
      <v-row align="start" justify="space-around" no-gutters>
        <v-col>
          <span
            style="font-weight: bold; font-size: 500%; color: #FFFFFF"
          >{{ Math.round((styrka/3.6)*10)/10 }} m/s</span>
        </v-col>
        <v-col cols="auto">
          <span>{{ vinkel }}</span>
        </v-col>
        <v-col cols="auto">
          <v-icon class="mr-8" :style="rotate">mdi-arrow-up</v-icon>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "Wind",
  rotate: "",
  styrka: "",
  vinkel: "",
  props: {
    Title: {
      type: String,
      required: true
    },
    Strength: {
      type: Number,
      required: true
    },
    Direction: {
      type: Number,
      required: true
    },
    Burst: {
      type: String,
      required: false
    }
  },
  created() {
    this.styrka = this.Convert_Strength(this.Strength, this.Direction);
    this.vinkel = this.Convert_Direction(this.Strength, this.Direction);
    this.makestyle(this.vinkel);

    setInterval(() => {
      this.styrka = this.Convert_Strength(this.Strength, this.Direction);
      this.vinkel = this.Convert_Direction(this.Strength, this.Direction);
      this.makestyle(this.vinkel);
    }, 1000);
  },
  methods: {
    Convert_Strength(styrka, vinkel) {
      let x = styrka * Math.cos((vinkel * Math.PI) / 180);
      let y = styrka * Math.sin((vinkel * Math.PI) / 180);
      let a = Math.sqrt(x * x + y * y);

      return Math.round(a);
    },
    Convert_Direction(styrka, vinkel) {
      let x = styrka * Math.cos((vinkel * Math.PI) / 180);
      let y = styrka * Math.sin((vinkel * Math.PI) / 180);
      let b = Math.atan2(x, y) * (180 / Math.PI);

      return Math.round(b);
    },
    makestyle(vinkel) {
      this.rotate = "transform: rotate(" + vinkel + "deg) scale(5);; ";
    }
  }
};
</script>

<style >
#arrow {
  transform: rotate(1deg);
}
</style>