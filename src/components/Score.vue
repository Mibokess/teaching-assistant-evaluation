<template>
  <div class="container score-container">
    <div class="row d-flex justify-content-center">
      <span class="stat-description">{{ description }}</span>
    </div>
    <div class="row">
      <div class="col stat-col d-flex justify-content-center">
        <span class="stat-label d-flex justify-content-center">
          <i v-bind:class="left"></i>
        </span>
      </div>

      <div class="col-8">
        <div class="progress">
          <div 
            class="progress-bar" 
            role="progressbar" 
            v-bind:style="{width: avg * 100 +'%'}" 
            v-bind:aria-valuenow="avg" 
            aria-valuemin="0" 
            aria-valuemax="1">
          </div>
        </div>
      </div>

      <div class="col stat-col d-flex justify-content-center">
        <span class="stat-label d-flex justify-content-center">
          <i v-bind:class="right"></i>
        </span>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Score',
  props: {
    description: String,
    left: String,
    right: String,
    avg: Number
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus">

@import '../assets/App.styl'

.stat-label
  color color4
  position absolute
  margin-top -1px
  text-align center

.stat-description
  color color4
  margin-bottom 2px

.score-container
  margin-bottom 8px

.progress-bar
  background-color color2

</style>
