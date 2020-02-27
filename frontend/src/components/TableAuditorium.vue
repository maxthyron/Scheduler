<template>
  <div class="auditoriums">
    <b-button variant="success" size="sm" class="m-1 auditorium-button" :key="auditorium.id" v-for="auditorium in auditoriums">{{auditorium.id}}</b-button>
  </div>
</template>

<script>
export default {
  name: 'TableAuditorium',
  props: {
    auditoriums: {
      type: null,
      required: true
    }
  }
}
</script>

<style scoped>
  .auditorium-button {
    width: 15vw;
    font-size: 3.5vw;
  }
</style>
