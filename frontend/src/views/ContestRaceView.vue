<template>
  <div id="app">
    <div class="mx-auto">
      <img class="title" src="../assets/title.png" />
      <img class="talent" :src="imageSrc" />
      <div :id="this.$category[this.pageNum].en" class="chart"></div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CryptoJS from "crypto-js";
import { toRaw } from "vue";
import * as echarts from "echarts";

export default {
  props: {
    pageNum: Number,
  },
  data() {
    return {
      contestData: "",
      token: this.$store.state.token,
    };
  },
  watch: {
    pageNum: function () {
      this.showChart();
    },
  },
  async mounted() {
    let account = CryptoJS.AES.decrypt(
      this.$store.state.token,
      import.meta.env.VITE_APP_SECRET_KEY
    ).toString(CryptoJS.enc.Utf8);
    if (["admin"].includes(account)) {
      alert(this.$category[this.pageNum].zh);
      this.showChart();
    } else {
      alert("您不是管理者");
    }
  },
  computed: {
    imageSrc() {
      return `../src/assets/${this.$category[this.pageNum].en}.svg`;
    },
  },
  methods: {
    async getData() {
      await axios
        .get(`./vote/race/${this.$category[this.pageNum].en}`)
        .then((res) => {
          this.contestData = toRaw(res.data.data);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async showChart() {
      var chartDom = document.getElementById(this.$category[this.pageNum].en);
      var myChart = echarts.init(chartDom);
      var option;
      await this.getData();
      let response = toRaw(this.contestData);
      var dataMap = response.value;
      var teams = response.teams;
      var hours = response.hours;
      var data_series = [];
      for (var i = 0; i < hours.length; i++) {
        data_series.push({ series: [{ data: dataMap[hours[i]] }] });
      }
      option = {
        baseOption: {
          timeline: {
            axisType: "category",
            height: 60,
            show: false,
            loop: false,
            autoPlay: true,
            playInterval: 500,
            label: {
              textStyle: {
                align: "center",
                baseline: "middle",
                fontSize: 35,
              },
            },
            controlStyle: {
              itemSize: 35,
            },
            data: hours,
          },
          title: {
            textStyle: {
              fontSize: 60,
            },
          },
          tooltip: {},
          grid: {
            top: 20,
            bottom: 130,
            right: 150,
            left: 200,
            tooltip: {
              trigger: "axis",
              axisPointer: {
                type: "shadow",
                label: {
                  show: true,
                  formatter: function (params) {
                    return params.value.replace("\n", "");
                  },
                },
              },
            },
          },
          yAxis: [
            {
              max: 4,
              type: "category",
              inverse: true,
              axisLabel: {
                fontSize: 36,
                color: "#005154",
              },
              data: teams,
              splitLine: { show: true },
            },
          ],
          xAxis: [
            {
              type: "value",
              axisLabel: {
                show: false,
                fontSize: 30,
                formatter: "{value} %",
                color: "#005154",
              },
              show: false,
              animationDuration: 1000,
              animationDurationUpdate: 2000,
            },
          ],
          series: [
            {
              name: this.$category[0].zh,
              type: "bar",
              realtimeSort: true,
              label: {
                show: true,
                precision: 2,
                position: "right",
                valueAnimation: true,
                fontFamily: "monospace",
                fontSize: 40,
                formatter: "{c}%",
              },
              itemStyle: { color: "#00a19b" },
            },
          ],
          animationDuration: 0,
          animationDurationUpdate: 600,
        },
        options: data_series,
      };
      option && myChart.setOption(option);
    },
  },
};
</script>

<style scoped>
#app {
  background-color: white;
  background-size: cover;
  background-position: left;
  padding: 60px 0 100px;
}
img.talent {
  max-width: 400px;
  width: 100%;
  display: block;
  margin: 0px auto;
  margin-top: 30px;
  margin-bottom: 40px;
}
img.title {
  max-width: 400px;
  width: 100%;
  display: block;
  margin: 0px auto;
  margin-bottom: 20px;
}
.chart {
  width: 100%;
  height: 600px;
  display: block;
}
h1 {
  font-size: 40px;
  text-align: center;
  margin-bottom: 1.5rem;
  color: #009ca6;
}

h3 {
  margin-bottom: 1.5rem;
  text-align: center;
}

p {
  line-height: 1rem;
}
.container {
  display: grid;
}
.btn-primary {
  background-color: #008c95 !important;
  border: 0px;
}
#title {
  font-size: 32px;
  font-weight: bold;
  color: #005154;
}
</style>
