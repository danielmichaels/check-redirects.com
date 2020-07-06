<template>
  <div id="results-error" class="container">
    <b-card>
      <b-card-text
        ><h2>
          {{ propData[0].error.reason }}
        </h2>
      </b-card-text>
      <b-card-text class="text-muted">
        <a :href="`${propData[0].error.url}`">{{ propData[0].error.url }}</a>
      </b-card-text>
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
