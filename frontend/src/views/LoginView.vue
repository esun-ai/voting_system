<template>
  <div id="app">
    <div class="login-page" v-cloak>
      <transition name="fade">
        <div v-if="!registerActive" class="wallpaper-login"></div>
      </transition>
      <div class="wallpaper-register"></div>
      <div class="container text-center">
        <img class="my-logo" src="../assets/my-logo.png" />
        <div class="row">
          <img class="kv-title" src="../assets/title.png" />
          <p class="prepare-word mt-3 text-center">最佳人氣 由你來選</p>
          <div class="">
            <div
              v-if="login_status == 0"
              class="card register text-center p-4"
              v-bind:class="{ error: errorShake }"
            >
              <h3 class="text-center mb-3">使用者登入</h3>
              <h6 style="text-align: left">帳號</h6>
              <input
                v-model="account"
                type="text"
                class="form-control"
                placeholder="admin"
                required
                pattern="[0-9]{5}"
              />
              <h6 style="text-align: left">密碼</h6>
              <input
                v-model="login_password"
                type="password"
                class="form-control"
                id="password-data"
                placeholder="12345678"
                required
              />
              <h6 v-if="errorShake" class="phone-verify">{{ login_msg }}</h6>
              <br />
              <button
                type="submit"
                class="btn btn-primary m-0"
                @click="doLogin"
                id="submit"
              >
                登入
              </button>
              <div class="mt-3 text-center">
                <div style="float: left">尚未註冊?&nbsp;</div>
                <router-link to="./userinfo"
                  ><div style="float: left">註冊</div></router-link
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { mapMutations } from "vuex";

export default {
  data() {
    return {
      // 切換登入=0; 註冊=1; 忘記密碼=2
      login_status: 0,

      // 帳號密碼
      account: "",
      login_password: "",

      // 登入訊息
      login_msg: "",

      // 控制 error animation
      errorShake: false,
    };
  },
  methods: {
    ...mapMutations(["login"]),
    // 使用者登入
    async doLogin() {
      if (this.account.length <= 4) {
        this.login_msg = "確認帳號至少 5 碼";
        this.errorShake = true;
      } else if (this.login_password.length <= 3) {
        this.login_msg = "請確認密碼至少4碼";
        this.errorShake = true;
      } else {
        let login_json = await axios
          .post("/login", {
            account: this.account,
            password: this.login_password,
          })
          .then((response) => {
            return response.data.data;
          })
          .catch((error) => {
            console.log(error);
            return 400;
          });
        if (login_json.status == 200) {
          this.login({ auth: this.account });
          this.$router.push({ name: "MenuView" });
        } else {
          this.errorShake = true;
          this.login_msg = "帳號或密碼錯誤";
        }
      }
      // 輸入錯誤就抖動3秒
      setTimeout(() => {
        this.errorShake = false;
      }, "3000");
    },
  },
};
</script>

<style scoped>
@import "../assets/css/component.css";
.my-logo {
  max-width: 90px;
  width: 100%;
  position: absolute;
  top: 30px;
  right: 30px;
  height: auto;
}
#app {
  background: #f5deb3;
  background-size: cover;
  background-position: left;
}
.kv-title {
  display: block;
  max-width: 400px;
  width: 100%;
  margin: 0 auto;
  height: auto;
  margin-bottom: 15px;
}
.prepare-word {
  font-size: 1.4em;
  color: #e66900;
  line-height: inherit;
  line-height: 1rem;
}
h6 {
  line-height: 1.4em;
}
p {
  line-height: 1rem;
}
#title {
  font-size: 26px;
  text-align: center;
  margin-bottom: 1rem;
  color: #009ca6;
}
.phone-number {
  margin-bottom: 0%;
}
.phone-verify {
  color: red;
  margin-top: 2%;
  margin-bottom: 0%;
}

input {
  margin-bottom: 10%;
}
.login-page {
  align-items: center;
  display: flex;
  height: 100vh;
}
.wallpaper-login {
  background-size: cover;
  height: 100%;
  position: absolute;
  width: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.wallpaper-register {
  background-size: cover;
  height: 100%;
  position: absolute;
  width: 100%;
  z-index: -1;
}

#password-data {
  margin-bottom: 0%;
}
.error {
  animation-name: errorShake;
  animation-duration: 0.3s;
}
@keyframes errorShake {
  0% {
    transform: translateX(-25px);
  }
  25% {
    transform: translateX(25px);
  }
  50% {
    transform: translateX(-25px);
  }
  75% {
    transform: translateX(25px);
  }
  100% {
    transform: translateX(0);
  }
}
[v-cloak] {
  display: none;
}
@media screen and (max-width: 568px) {
  .my-logo {
    max-width: 10vh;
    top: 16px;
    right: 16px;
  }
  .content {
    transform: translateY(-80px);
  }
  .kv-title {
    max-width: 300px;
  }
  .prepare-word {
    font-size: 1.2em;
  }
}
@media screen and (max-width: 340px) {
  .kv-title {
    max-width: 300px;
  }
  .prepare-word {
    font-size: 1em;
    margin-top: 0 !important;
  }
  .card {
    margin: 0;
  }
}
</style>
