<template>
  <header>

  <nav class="navbar" id="top-nav">
      <clock-component @updateClock = "updateClock"> </clock-component>
      <div class="container-fluid justify-content-center p-0">
        <div id="tip-description">
          <p v-if="duringEvent!==2 && pageNum===0" style="text-align:center">每人請投2票，但需投不同隊伍</p>
          <p v-if="duringEvent!==2 && pageNum===1" style="text-align:center">每人限投1票</p>
          <p v-else style="text-align:center"></p>
        </div>
        <div class="w-100 d-flex justify-content-center p-0">
            <router-link v-for="(route, index) in childRoutes.slice(0, -1)" :key="index" class="tab" :to="{name: route.name}" @click="pageClick(index)"><b-button pill variant="primary" class="tab-btn">{{ this.$category[index].zh }}</b-button></router-link>
            <router-link class="tab" :to="{name:'PreView'}"><b-button pill variant="primary" class="tab-btn" >投票紀錄</b-button></router-link>
        </div>
      </div>
  </nav> 
 
  </header>
  <body>
    <router-view 
      :duringEvent = "duringEvent"
      :pageNum = "pageNum"
      @vote="update">
    </router-view>
  </body>
</template>

<script>
import ClockComponent from "@/components/ClockComponent.vue"
import CryptoJS from "crypto-js";

export default {
  components: {
    ClockComponent,
  },
  data() {
    return {
      // 使用者登入帳號
      account : CryptoJS.AES.decrypt(this.$store.state.token, import.meta.env.VITE_APP_SECRET_KEY).toString(CryptoJS.enc.Utf8),
      // 0=活動尚未開始; 1=活動進行中; 2=活動結束
      duringEvent: 0,
      pageNum: 0,
      targetInfo: [],
      childRoutes: this.$router.options.routes.filter(route => route.path.startsWith('/home'))[0].children
    }
  },
  methods:{
    pageClick (pageNum) {
      this.pageNum = pageNum
    },
    // 更新 during event 的狀態
    updateClock(val){
      this.duringEvent = val
    },
    update(val){
      this.targetInfo = {...this.$store.state.votedObject}
      if (this.$category[this.pageNum].en in this.targetInfo === false) {
        this.targetInfo[this.$category[this.pageNum].en] = {
          target: '',
          status: false
        }
      }
      this.targetInfo[this.$category[this.pageNum].en].target += ` ${val.target}`
      this.targetInfo[this.$category[this.pageNum].en].status = val.status  
      this.$store.commit('setVotedObject', this.targetInfo)
    }
  },
}
</script>

<style scoped>
@import '../assets/css/component.css';
header + body{
    padding: 30px;
    padding-top: 240px;
}

#tip-description{
  width: 110%;
  font-size: 15px;
  margin:0%;
}

#top-nav {
  position: fixed;
  background-color:#F4F8FA;
  border-bottom:5px solid rgb(255, 255, 255);
  height:240px;
  width: 100%;
  font-size: 15px;
  padding-left:20px;
  padding-right:20px;
  text-align: center;
  z-index:87;
}

.render-btn{
  font-size: 16px;
  border-radius: 5px;
  margin-right: 3px;
  margin-left: 3px;
  margin-top: 3px;
  margin-bottom: 3px;
}
.router-link{
  text-decoration:none;
  color:black;
}
@media screen and (max-width:576px){
  #top-nav {
    height: 300px;
  }
  header + body{
    padding-top: 300px;
}
}
</style>