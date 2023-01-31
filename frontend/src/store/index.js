import { createStore } from "vuex";
import Cookie from "vue-cookies";
import CryptoJS from "crypto-js";

let secret_key = import.meta.env.VITE_APP_SECRET_KEY;

// Create a new store instance.
const store = createStore({
  state: {
    // 儲存token
    token: Cookie.get("token"),
    votedObject: {},
    checkStatus: false,
    contestsObject: {}
  },

  mutations: {
    // 修改token，並將token存入Cookies
    login: function (state, payload) {
      // Encrypt 加密
      let encrypt_token = CryptoJS.AES.encrypt(
        payload.auth,
        secret_key
      ).toString();
      // 修改這兩個變數的值
      state.token = encrypt_token;
      // 往cookie中寫資料
      Cookie.set("token", encrypt_token);
    },
    logout: function () {
      // 往cookie中清除資料
      Cookie.remove("token");
    },
    setVotedObject: function (state, payload) {
      state.votedObject = payload;
    },
    setCheckStatus: function (state, payload) {
      state.checkStatus = payload;
    },
    setContestsObject: function (state, payload) {
      state.contestsObject = payload;
    }
  },
  actions: {},
});

export default store;
