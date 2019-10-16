<template>
  <div class="container login-container">
    <form>
      <div class="form-group">
        <label for="inputUsername">Username</label>
        <input v-model="username" type="text" class="form-control" id="inputUsername">
      </div>
      <div class="form-group">
        <label for="inputPassword">Password</label>
        <input v-model="password" type="password" class="form-control" id="inputPassword">
      </div>
      <button v-on:click="login()" class="btn btn-primary btn-login">Log In</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  props: {
  },
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login() {
      axios.get('/api/login/?format=json&username=' + this.username + '&password=' + this.password)
      .then(function (response) {
        console.log("ok")
        this.$router.push({ path: '/' })
      })
      .catch(function (error) {
        console.log("Wrong username/password")
        alert("Wrong username/password")
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus">

@import '../assets/App.styl'

.login-container
  max-width 30rem

.btn-login
  width 100px
  background-color color1
  border-radius border-round
  &:hover
    background-color color1-hover


</style>
