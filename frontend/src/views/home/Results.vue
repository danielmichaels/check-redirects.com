<template>
  <div id="results" class="container-fluid">
    <b-card class="mt-3" header="responseData from Results.vue">
      <pre class="mt-0">
      {{ propData }}
          </pre
      >
    </b-card>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Index extends Vue {
  @Prop({
    type: Array,
  })
  propData!: string[];

  constructor() {
    super();
    console.log(this.propData);
  }
}
</script>

<style scoped></style>
