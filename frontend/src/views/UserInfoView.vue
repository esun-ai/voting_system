<template>
  <div id="app">
    <div class="login-page" v-cloak>
      <div class="container">
        <div class="row">
          <div
            class="col-lg-4 col-md-6 col-sm-8 mx-auto"
            id="outer-space"
            v-bind:class="{ error: errorShake }"
          >
            <div class="card login">
              <img class="kv-title" src="../assets/title.png" />
              <h3 style="margin-bottom: 1%">使用者註冊</h3>
              <div class="mx-auto" style="margin-bottom: 2%"></div>
              <br />
              <div>
                <h6 class="input-title">帳號</h6>
                <input
                  v-model="account"
                  type="text"
                  class="form-control input-data"
                  placeholder="帳號至少 5 碼"
                  style="msgStyle"
                />
                <h6 v-if="errorShake" class="data-verify">{{ account_msg }}</h6>
                <h6 class="input-title">密碼</h6>
                <input
                  v-model="password"
                  type="password"
                  class="form-control input-data"
                  placeholder="密碼輸入大於 4 碼"
                />
                <h6 v-if="errorShake" class="data-verify">
                  {{ password_msg }}
                </h6>
                <h6 class="input-title">確認密碼</h6>
                <input
                  v-model="confirm_password"
                  type="password"
                  class="form-control input-data"
                  placeholder="再次確認您的密碼"
                />
                <h6 v-if="errorShake" class="data-verify">
                  {{ confirm_password_msg }}
                </h6>
                <h6 style="margin-bottom: 1%; color: red">送出後不可修改！</h6>
                <button
                  type="submit"
                  class="btn btn-primary"
                  @click="send_user"
                  id="submit"
                >
                  送出
                </button>
                <div style="margin-top: 2%">
                  <div style="float: left">已經註冊過了？&nbsp;</div>
                  <router-link to="./login"
                    ><div style="float: left">登入</div></router-link
                  >
                </div>
                <br />
                <br />
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
export default {
  data() {
    return {
      account: "",
      account_msg: "",
      password: "",
      password_msg: "",
      confirm_password: "",
      confirm_msg: "",
      errorShake: false,
    };
  },
  methods: {
    // 確認使用者資訊 (很多 condition)，如果錯誤，則 error shake 觸發 error shake 特效會在 3 秒後解除，若正確則向後端發送基本資料，建立 user
    async send_user() {
      if (this.account.length <= 4) {
        this.account_msg = "確認帳號至少 5 碼";
        this.errorShake = true;
      } else if (this.password.length <= 3) {
        this.password_msg = "請輸入大於 4 碼的密碼";
        this.errorShake = true;
      } else if (this.confirm_password === "") {
        this.confirm_password_msg = "請輸入確認密碼";
        this.errorShake = true;
      } else if (this.confirm_password !== this.password) {
        this.confirm_password_msg = "密碼 & 確認密碼不相符";
        this.errorShake = true;
      } else {
        let userinfo_data = await axios
          .post("/users/userinfo", {
            account: this.account,
            password: this.password,
            is_admin: false,
            is_active: true,
          })
          .then((response) => {
            return response;
          })
          .catch((error) => {
            return error;
          });
        if (
          userinfo_data.status == 200 &&
          userinfo_data.data.data === "註冊成功"
        ) {
          this.$router.push({ name: "LoginView" });
          alert("註冊成功，請登入！");
        } else if (userinfo_data.data.message == "success") {
          alert(userinfo_data.data.data);
        } else {
          alert("其他未知錯誤，請通知管理者");
        }
      }
      setTimeout(() => {
        this.errorShake = false;
        this.name_msg = "";
        this.account_msg = "";
        this.password_msg = "";
        this.confirm_password_msg = "";
      }, "3000");
    },
  },
};
</script>

<style scoped>
@import "../assets/css/component.css";
#app {
  background: #f5deb3;
  background-size: cover;
}
h3 {
  margin-bottom: 1.5rem;
  text-align: center;
}

h6 {
  margin-left: 1%;
  margin-top: 4%;
  margin-bottom: 1%;
}

p {
  line-height: 1rem;
}
.input-title {
  text-align: left;
}
.input-data {
  margin-bottom: 0%;
}

.card {
  margin-top: 4%;
  width: 100%;
  height: 100%;
  padding: 20px;
}
.check-is_esun-btn {
  font-size: 100%;
  color: white;
  background-color: #4882bb;
  height: 40px;
  width: 40%;
  max-width: 150px;
  margin-right: 2%;
  margin-left: 2%;
  border-radius: 5px;
}
.data-verify {
  color: red;
  margin-top: 1%;
  margin-bottom: 0%;
}
.login-page {
  text-align: center;
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
.btn-primary {
  background-color: #008c95 !important;
  border: 0px;
}
.check-is_esun-btn {
  font-size: 15px;
}
#title {
  font-size: 26px;
  text-align: center;
  margin-bottom: 1rem;
  color: #009ca6;
}
#outer-space {
  width: 100%;
  max-width: 550px;
}
#submit {
  margin-top: 10px;
  margin-bottom: 10px;
  text-align: center;
  line-height: 25px;
  width: 100%;
  height: 40px;
  border-radius: 10px;
  letter-spacing: 5px;
}
#submit-send {
  position: absolute;
  top: 0;
  border-radius: 5px;
  right: 0px;
  z-index: 2;
  border: none;
  top: 2px;
  height: 30px;
  cursor: pointer;
  color: white;
  background-color: #1e90ff;
  transform: translateX(2px);
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
</style>
