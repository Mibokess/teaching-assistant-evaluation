<template>
  <div class="d-flex flex-column">
    <div v-if="errored">
      <p>Error receiving the questions</p>
    </div>
    <div v-else="">
      <div v-if="this.questions.length > 0">
        <div class="card card-survey mx-auto" style="max-width: 24rem;">
          <div class="card-body vertical-center">
            <p class="card-text container">
              {{ questions[0].label }}
            </p>
          </div>
          <div class="d-flex flex-row card-footer bg-transparent border-success">
            <button 
              type="button" 
              class="btn btn-primary btn-vote btn-vote-left"
              v-on:click="vote('P')"
            >
              {{ questions[0].positive }}
            </button>
            <button 
              type="button" 
              class="btn btn-primary btn-vote btn-vote-right"
              v-on:click="vote('N')"
            >
              {{ questions[0].negative }}
            </button>
          </div>
        </div>
        <div>
          <span class="text-muted">{{ this.questions.length }} remaining</span>
        </div>
      </div>
      <div v-else-if="endVisible">
        <div class="d-flex flex-column align-items-center mx-auto" style="max-width: 80%">
          <img src="../assets/finish.svg" style="max-width: 100%"/>
          <span class="font-weight-bold my-4" style="font-size: 1.4rem">Thank you for providing feedback about your TA!</span>
            <button type="button" class="btn btn-blue" v-on:click="goHome()">Home</button>
        </div>
      </div>
    </div>
    <div>
      <button type="button" class="btn btn-qr" style="max-width: 4rem" data-toggle="modal" data-target="#myModal">
        <img class="w-100 h-100" src="../assets/qr-code.svg"/>
      </button>
    </div>
    <div id="myModal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-body">
                <qrcode v-bind:value="url" :options="{ width: 400 }"></qrcode>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Survey',
  methods: {
    vote(answer) {
      axios.post('/api/votes/', {
        session: this.$route.params.Sid,
        question: this.questions[0].id,
        opinion: answer
      });

      console.log(this.$route.params.Sid)
      console.log(this.questions[0].id)
      console.log(answer)

      this.questions.shift();
      this.endVisible = true;
    },
    goHome() {
      this.$router.push({ path: '/' })
    },
  },
  data() {
    return {
      questions: [
      ],
      url: '',
      endVisible: false
    }
  },
  mounted() {
    this.url = window.location.href;
    axios.get("/api/questions?format=json")
      .then(res => {
        this.questions = res.data;
      })
      .catch(err => {
        this.error = true;
      })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus">

@import '../assets/App.styl'

.btn-vote 
  width 100%
  border-top-left-radius 0
  border-top-right-radius 0
  border 4px solid #223872
  border-top 0

.btn-vote-left 
  border-bottom-right-radius 0
  border-bottom-left-radius border-round
  left 0
  background-color #488ED5
  font-size 1.2em
  font-weight bold
  border-right-width 2px
  &:hover
    text-decoration none
    background-color #2B75BF


.btn-vote-right 
  border-bottom-left-radius 0
  border-bottom-right-radius border-round
  background-color #488ED5
  font-size 1.2em
  font-weight bold
  border-left-width 2px
  &:hover
    text-decoration none
    background-color #2B75BF

.btn-blue 
  background-color #488ED5
  font-size 1.2em
  font-weight bold
  color white
  &:hover
    text-decoration none
    background-color #2B75BF

.card-footer 
  position relative
  padding 0
  min-height 15vh
  border 0

.card-text
  color color4

.card-survey
  padding 0
  min-height 60vh
  border 0
  font-weight bold
  font-size 1.2em
  &:hover
    background-color color1

.vertical-center
  display flex
  align-items center

.btn-qr
  margin-top 10px

</style> 