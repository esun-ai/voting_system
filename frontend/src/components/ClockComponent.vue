<template>
  <form class="d-flex">
    <router-link class="router-link" :to="{ name: 'MenuView' }">
      <button class="" id="return-btn" type="submit">◄ 返回</button>
    </router-link>
  </form>
  <div class="container-fluid justify-content-center mt-4">
    <div id="title">玉山 <span>投票系統</span></div>
  </div>
  <div class="container-fluid justify-content-center">
    <div id="time-middle">
      <p v-if="duringEvent == 1" class="status mt-2 ing">• 投票進行中 •</p>
      <p v-else-if="duringEvent == 0" class="status mt-2 end">
        • 投票尚未開始 •
      </p>
      <p v-else class="status mt-2 end">• 投票已結束 •</p>
    </div>
  </div>
  <div class="container-fluid justify-content-center">
    <div id="time-middle">目前時間：&nbsp;&nbsp;{{ Local_time }}</div>
  </div>
  <div class="container-fluid justify-content-center">
    <div id="time-middle" v-if="duringEvent != 2">
      {{
        duringEvent === 0 ? "距離活動開始剩餘" : "距離活動結束剩餘"
      }}：&nbsp;&nbsp;{{ time_left_object.hours_remaining }}
      <span class="minute-second">時&nbsp;&nbsp;</span>
      {{ time_left_object.minutes_remaining }}
      <span class="minute-second">分&nbsp;&nbsp;</span>
      {{ time_left_object.seconds_remaining }}
      <span class="minute-second">秒</span>
    </div>
    <div v-else>
      <!-- empty -->
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  emits: ["updateClock"],
  data() {
    return {
      // 注意 month 0= January, ... 是從 0 開始算！
      // current: new Date(),
      // 說明: 當 current time < start 則活動尚未開始 duringEvent = 0
      // 當 start < current time < end 則活動正在進行 duringEvent = 1
      // 當 end < current time 則活動結束 duringEvent = 2
      current: new Date(),
      start: new Date().setHours(13, 0, 0, 0),
      end: new Date().setHours(17, 30, 0, 0),
      duringEvent: 0,
    };
  },
  computed: {
    time_left_object: {
      get() {
        let time_span;
        if (this.duringEvent == 0) {
          time_span = (this.start - this.current) / 1000;
        } else if (this.duringEvent == 1) {
          time_span = (this.end - this.start) / 1000;
        } else {
          time_span = 0;
        }

        let hours_remaining = Math.floor(time_span / 3600);
        let minutes_remaining = Math.floor(
          time_span / 60 - hours_remaining * 60
        );
        let seconds_remaining = Math.floor(
          time_span - hours_remaining * 3600 - minutes_remaining * 60
        );
        let return_object = {
          time_span: time_span,
          hours_remaining: hours_remaining,
          minutes_remaining: minutes_remaining,
          seconds_remaining: seconds_remaining,
        };
        return return_object;
      },
    },
    Local_time: {
      get() {
        return this.current.toLocaleString();
      },
    },
  },
  methods: {
    //向後端要 current time，並存在current time
    async getCurrentTime() {
      let time = await axios.get("./vote/now");
      this.current = new Date(time.data.data.now);
      this.start = new Date(time.data.data.start_time);
      this.end = new Date(time.data.data.end_time);
    },

    // 每秒中 current time + 1, 並依據 current time 與 start, end 之間的關係，更動 duringEvent
    countDownTimer() {
      setTimeout(() => {
        this.checkEventStatus();
        this.countDownTimer();
      }, 1000);
    },

    checkEventStatus() {
      this.current = new Date(
        this.current.getFullYear(),
        this.current.getMonth(),
        this.current.getDate(),
        this.current.getHours(),
        this.current.getMinutes(),
        this.current.getSeconds() + 1
      );

      if (this.current >= this.start && this.current <= this.end) {
        this.duringEvent = 1;
        this.$emit("updateClock", this.duringEvent);
      } else if (this.current >= this.end) {
        this.duringEvent = 2;
        this.$emit("updateClock", this.duringEvent);
      }

      if (this.duringEvent === 1) {
        this.start = this.current;
      }
    },
  },
  created() {
    this.getCurrentTime();
    this.countDownTimer();
  },
};
</script>

<style scoped>
@import "../assets/css/component.css";
.status {
  font-size: 18px;
  border-bottom: 1px solid;
  font-weight: bold;
}
.ing {
  color: #00a19b;
}
.end {
  color: #acacac;
}
#return-icon {
  width: 65px;
  max-width: 300%;
}

#return-btn {
  position: absolute;
  top: 13px;
  left: -5px;
  width: 100px;
  font-size: 18px;
  padding: 0px;
  color: #00a19b;
}

#title {
  font-size: 32px;
  font-weight: bold;
  color: #005154;
}
#tip-description {
  font-size: 10px;
  margin: 0%;
}
#remind-title {
  font-size: 20px;
  height: auto;
}

#time-middle {
  display: flex;
}

.minute-second {
  font-size: 15px;
}

.router-link {
  text-decoration: none;
  color: black;
}
@media screen and (max-width: 576px) {
  #title span {
    display: block;
  }
}
</style>
