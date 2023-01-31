<template>
  <div class="text-center">
    <div class="card p-4" v-for="categoryKey in this.$category" :key="categoryKey.en">
      <div style="text-align: center" id='sing'>
        <div class="display-result">{{ categoryKey.zh }}</div>
        <div class="display-result">&nbsp;</div>
        <div v-if="this.previews[categoryKey.en].status" class="display-result" id="voted">
          您投票給：{{ this.previews[categoryKey.en].target }}
        </div>
        <div v-else class="display-result" id="not-vote">尚未投票</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CryptoJS from "crypto-js";

export default {
  name: "PreView",
  props: {
    duringEvent: Number
  },
  data() {
    return {
      account: CryptoJS.AES.decrypt(
        this.$store.state.token,
        import.meta.env.VITE_APP_SECRET_KEY
      ).toString(CryptoJS.enc.Utf8),
      previews: {}
    };
  },
  watch: {
    '$route': 'checkVotedWho'
  },
  methods: {
    async checkVotedWho() {
      if (this.$store.state.checkStatus === false) {
        const vote_2_sing = await axios.get("/vote/who", {
          params: { account: this.account, gid: this.$category[0].zh },
        });
        const vote_2_talent = await axios.get("/vote/who", {
          params: { account: this.account, gid: this.$category[1].zh },
        });
        this.sing_vote2who = vote_2_sing.data.data;
        this.talent_vote2who = vote_2_talent.data.data;
        if (this.sing_vote2who !== "查無資訊") {
          this.previews[this.$category[0].en]['status'] = true;
          this.previews[this.$category[0].en]['target'] = this.sing_vote2who;
        }
        if (this.talent_vote2who !== "查無資訊") {
          this.previews[this.$category[1].en]['status'] = true;
          this.previews[this.$category[1].en]['target'] = this.talent_vote2who;
        }
        this.$store.commit("setVotedObject", this.previews);
        this.$store.commit("setCheckStatus", true);
      }
      else {
        this.previews = this.$store.state.votedObject;
      }
    }
  },
  created() {
    this.$category.forEach((category) => {
      this.previews[category.en] = {
        status: false,
        target: ""
      }
    });
    this.checkVotedWho();
  },
  computed: {
    categoryKeys () {
      return Object.keys(this.previews)
    }
  }
};
</script>

<style scoped>
@import "../assets/css/component.css";
.display-result {
  display: inline-block;
}
.not-vote {
  padding: 3%;
}
#warning {
  color: red;
  margin-bottom: 1%;
  font-size: 10px;
  font-weight: bold;
}
#submit-result-btn {
  color: black;
  background-color: rgba(223, 255, 173, 0.411);
  width: 50%;
  max-width: 150px;
  border-radius: 5px;
  padding: 1%;
  margin-top: 5px;
  margin-bottom: 5px;
}
#cannot-submit-btn {
  color: black;
  background-color: rgba(173, 173, 173, 0.411);
  width: 50%;
  max-width: 150px;
  border-radius: 5px;
  padding: 1%;
}
#submit-result-btn:active {
  background-color: rgb(121, 206, 99);
}

#vote {
  width: 100%;
  padding: 3%;
  font-weight: bold;
}
#voted {
  color: #00a19b;
  display: block;
  background-color: #fff;
  font-weight: bold;
  font-size: 20px;
  margin-top: 10px;
}

#not-vote {
  color: #acacac;
  display: block;
  background-color: #fff;
  font-weight: bold;
  font-size: 20px;
  margin-top: 10px;
}
#sing {
}
#talent {
}
@media screen and (min-width: 1080px) {
  #voted {
    height: 60px;
  }
  #not-vote {
    height: 60px;
  }
}
</style>
