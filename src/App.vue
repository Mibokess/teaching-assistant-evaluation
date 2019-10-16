<template>
  <div id="app">
    <div class="d-flex flex-row justify-content-center w-100" style="margin-bottom: 1.5rem;">
      <div class="d-flex flex-row justify-content-center page-header my-3" style="z-index: 2; max-width: 40rem;" v-on:click="goHome()">
        <div class="page-title w-100 d-flex flex-row justify-content-start w-100">
          <button type="button" class="btn p-0" style="margin-left: 25px;">
            <img class="w-0 p-0" src="./assets/arrow-left-circle.svg"/>
          </button>
          <div class="relative flex-grow-1">
            <span class="badge-pill bg-color1 text-white">TA<span class="align-top" style="font-size: 0.8em;">+</span></span>
            <span class="d-none d-md-inline ml-4" style="font-variant: small-caps;">Evaluation Tool</span>
          </div>
          <span style="width: 50px;"></span>
        </div>
      </div>
    </div>
    <div class="mx-auto" style="max-width: 50rem"> 
      <router-view/>
    </div>
  </div>
</template>

<script>

// let axiosDefaults = require('axios/lib/defaults');
// axiosDefaults.baseURL = 'https://happy-honeyberries.svis.ethz.ch';

export default {
  name: 'app',
  methods: {
    goHome() {
      this.$router.push({ path: '/' })
    }
  }
}
</script>

<style lang="stylus">

@import './assets/App.styl'

#app {
  font-family: Helvetica, 'Avenir', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding-top: 100px;
  background: color4;

  min-height 100vh
}

  .page-header
    position absolute
    top 0
    height 80px
    width 100vw

  .page-title
    margin-top 10px
    max-width 50rem
    font-size 2.5em

  .bg-color1 {
    background: color1;
  }

  .bg-hover1:hover {
    background: color1-hover;
  }

  .list-group-item {
    background: color4!important;
  }

  .text-white {
    color: color4!important;
  }

  button {
    transition: all .2s;
  }

  .bg-color1 input::placeholder{
    color: rgba(241, 241, 241, 0.75);
  }

  input + i {
    color: color4;
    transition: all 0.2s;
  }

  input:placeholder-shown + i {
    color: rgba(241, 241, 241, 0.75);
  }

  .fa:before {
    display: inline-block;
    font-size: 1.2em;
    margin-top: .12em;
  }
</style>
