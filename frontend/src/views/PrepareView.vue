<template>
  <div id="app">
    <div class="login-page" v-cloak>
      <transition name="fade">
        <div class="wallpaper-login"></div>
      </transition>
      <div class="wallpaper-register"></div>
      <div class="container">
        <img class="my-logo" src="../assets/my-logo.png" />
        <div class="content">
          <img class="kv-title" src="../assets/title.png" />
          <p class="prepare-word mt-3 text-center">活動尚未開始，敬請期待</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@-webkit-keyframes fk-fade-up-10 {
  0%,
  10% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0px);
  }
}

@keyframes fk-fade-up-10 {
  0%,
  10% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0px);
  }
}

#app {
  background-color: #f5deb3;
  background-size: cover;
  background-position: left;
}
.content {
  transform: translateY(-100px);
}
.kv-title {
  display: block;
  max-width: 370px;
  width: 100%;
  margin: 0 auto;
  height: auto;
  margin-bottom: 30px;
  -webkit-animation: fk-fade-up-10 1.3s cubic-bezier(0.68, -0.55, 0.265, 1.55) 1;
  animation: fk-fade-up-10 1.3s cubic-bezier(0.68, -0.55, 0.265, 1.55) 1;
}
.prepare-word {
}
.my-logo {
  max-width: 90px;
  width: 100%;
  position: absolute;
  top: 30px;
  right: 30px;
  height: auto;
}
p {
  font-size: 1.4em;
  color: #e66900;
  line-height: inherit;
  line-height: 1rem;
  -webkit-animation: fk-fade-up-10 1.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 1;
  animation: fk-fade-up-10 1.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 1;
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
.card {
  padding: 20px;
  padding-bottom: 0px;
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
.btn-primary {
  background-color: #008c95 !important;
  border: 0px;
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
    max-width: 400px;
  }
  .prepare-word {
    font-size: 1.2em;
  }
}
@media screen and (max-width: 340px) {
  .kv-title {
    max-width: 176px;
  }
  .prepare-word {
    font-size: 1em;
    margin-top: 0 !important;
  }
}
</style>
