<template>
    <div class="card mx-auto" style="max-width: 40rem">
        <slot name="header"></slot>
        <div name="body" class="card-body">
            <slot></slot>
        </div>
        <slot name="footer"></slot>
    </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
  },
  data() {
    return {
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus">

@import '../assets/App.styl'

.card
  background-color color1
  padding-left 20px
  padding-right 20px
  &:hover
    background-color color1-hover
  border-radius border-round !important
  transition: all .2s;

</style>
