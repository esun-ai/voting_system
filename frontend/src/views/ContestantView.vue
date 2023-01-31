<template v-if="this.pageNum!==99">
  <div class="home text-center">
    <div class="card" v-for="(image,index) in imageObject" :key="index">
      <div class="p-4 rounded mx-auto">
        <img class="mx-auto mb-4" :src="image.url" :alt="index" :key='index'/>
        <div class="description" style="text-align: left">
          <div>• 表演順序： {{image.description.tid}}</div>
          <div>• 表演名稱： {{image.description.show_name}}</div>
          <div>• 表演者： {{image.description.names}}</div>
          <div>• 表演形式： {{image.description.show_type}}</div>
          <br>
          <div style="text-align: center;">
            <button class="action-btn" v-if="duringEvent==0" id="cant-vote">尚未開始</button>
            <button class="action-btn" v-else-if="duringEvent==1 && (image.voted || image.done)" id="cant-vote">已完成投票</button>
            <button class="action-btn" v-else-if="duringEvent==1 && !image.done" id="vote" data-bs-toggle="modal" data-bs-target="#staticBackdrop2" @click="clickVote(image.description.show_name, image.description.tid)">投票</button>
            <button class="action-btn" v-else id="cant-vote">投票截止</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Modal -->
  <div class="modal fade" id="staticBackdrop2" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title" id="staticBackdropLabel">請確認您的{{this.$category[this.pageNum].zh}}投票</h3>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
            投票給：「{{this.contestantPerson}}」<br>
            點擊確認即成功投票並無法重新投票
        </div>
        <div class="modal-footer justify-content-center">
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="vote">是</button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">否</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CryptoJS from "crypto-js";
export default {
  props:{
    duringEvent: Number,
    pageNum: Number
  },
  data(){
    return{
        headers: {'token': import.meta.env.VITE_APP_TOKEN},
        account: CryptoJS.AES.decrypt(this.$store.state.token, import.meta.env.VITE_APP_SECRET_KEY).toString(CryptoJS.enc.Utf8),
        contestantPerson: "",
        contestantId: 0,
        contestantObject : [],
        voted: false,
        imagePath: [ new URL('@/assets/contestant.png', import.meta.url).href,
                      new URL('@/assets/contestant.png', import.meta.url).href,
                    ],
        imageObject: [],
    }
  },
  watch:{
    "$route": "createImageObject"
  },
  methods:{
    delay(time) {
      return new Promise(resolve => setTimeout(resolve, time));
    },
    async vote(){
      if(this.voted){
        let response = await axios.post("/vote/vote",{
                                        "account": this.account,
                                        "tid": this.contestantId,
                                        "gid": this.$category[this.pageNum].zh
                                      }, { headers: this.headers})
        if (response.data.message === "stop"){
          alert ("投票時間已截止！")
        }
        this.$emit('vote',{
          "target":this.contestantPerson,
          "status":this.voted,
          "targetId":this.contestantId} )
        await this.delay(300);
        await this.getInfo();
        this.createImageObject()
      }
    },
    getContestFromStore(){
      this.contestantObject = this.$store.state.contestsObject[this.$category[this.pageNum].en]
    },
    async getInfo(){
      let contestantData = await axios.post("./teams/get_menu", {
                                       "gid": this.$category[this.pageNum].zh,
                                       "account": this.account
                                      }, { headers: this.headers})
      this.contestantObject = contestantData.data.data
      let tmp = this.$store.state.contestsObject
      tmp[this.$category[this.pageNum].en] = contestantData.data.data
      this.$store.commit('setContestsObject', tmp)
    },
    clickVote(person, tid){
      this.voted = true
      this.contestantPerson = person
      this.contestantId = tid
    },
    cancelVote(){
      this.voted = false
      this.contestantPerson = ""
      this.contestantId = 0
    },
    async createImageObject(){
      this.$nextTick(async () => {
        if (this.$category[this.pageNum].en in this.$store.state.contestsObject){
          this.getContestFromStore()
        }
        else{
          await this.getInfo()
        }
        this.imageObject = []
        for(let i=0; i<this.contestantObject.length; i++){
          let tempName = this.contestantObject[i].name;
          let names = ""
          for(let j=0; j<tempName.length; j++){
            names += tempName[j]
            if (j !=tempName.length-1){
              names += " ";
            }
          }
          this.imageObject.push(
            {
              url:this.imagePath[i],
              voted: this.contestantObject[i].voted,
              done: this.contestantObject[i].done,
              alt:"參賽者圖片",
              description:{
                "gid": this.contestantObject[i].gid,
                "tid": this.contestantObject[i].tid,
                "show_name": this.contestantObject[i].show_name,
                "names": names,
                "show_type": this.contestantObject[i].show_type,
              },
            }
          )
        }
      })
    }

  },
  created(){
    this.createImageObject();
  }
}
</script>

<style scoped>
@import '../assets/css/component.css';
@media screen and (min-width:1024px){
  .card img{
  height: 200px;
}
}
</style>

