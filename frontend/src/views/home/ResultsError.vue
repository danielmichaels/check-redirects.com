<template>
  <div id="results-error" class="container">
    <b-card>
      <b-card-text
        ><h2>
          {{ propData[0].error.reason }}
        </h2>
      </b-card-text>
      <b-card-text class="text-muted">
        Requested Resource:
        <a target="_blank" :href="`${propData[0].error.url}`">{{ propData[0].error.url }}</a>
      </b-card-text>
      <b-button v-b-toggle="`collapse-errors`" class="m-1 bg-primary">
        Possible Causes
      </b-button>
      <b-collapse id="collapse-errors">
        <b-list-group flush>
          <li class="list-group-item">
            Incorrectly entered domain, or the domain no longer exists
          </li>
          <li class="list-group-item">
            Requested resource resides within private address space, or is being served locally
          </li>
          <li class="list-group-item">
            Firewall or proxy settings exist preventing resource resolution
          </li>
        </b-list-group>
      </b-collapse>
    </b-card>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IResultError } from '@/interfaces/results';

@Component
export default class Index extends Vue {
  @Prop({
    type: Array,
  })
  propData!: IResultError[];

  constructor() {
    super();
  }
}
</script>

<style scoped></style>
