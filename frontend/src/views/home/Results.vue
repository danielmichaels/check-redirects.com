<template>
  <div id="results" class="container">
    <div v-if="propData.length > 0">
      {{ finalUrl() }}
      <div class="">
        <h3>click the link here</h3>
        <b-button block variant="primary" :href="`${finalRedirectUrl}`" target="_blank">{{
          finalRedirectUrl
        }}</b-button>
      </div>

      <!--  branch out table into its own component    -->
      <div class="container">
        <h3>Summary</h3>
        <b-table
          :key="propData.id"
          striped
          stacked="sm"
          aria-busy="true"
          head-variant="light"
          :items="propData"
          :fields="fields"
          :tbody-tr-class="rowClass"
        ></b-table>
      </div>
      <div v-for="prop in propData" :key="prop.id">
        <div class="container">
          <h4>
            Redirects to: <a href="`${prop.url}`">{{ prop.url }}</a>
          </h4>
          <h4>
            <small> IP Address: {{ prop.ipaddr }} </small>
          </h4>
          <div class="row">
            <div class="col-sm">
              <b-card class="text-left">
                <h5><small>Status Code</small></h5>
                <b-card-text>{{ prop.status_code.code }}</b-card-text>
              </b-card>
            </div>
            <div class="col-sm">
              <b-card class="text-left">
                <h5><small>Status Message</small></h5>
                <b-card-text>{{ prop.status_code.phrase }}</b-card-text>
              </b-card>
            </div>
            <div class="col-sm">
              <b-card class="text-left">
                <h5><small>Latency</small></h5>
                <b-card-text>{{ prop.time_elapsed }}ms</b-card-text>
              </b-card>
            </div>
          </div>
        </div>
        <div>
          <b-button v-b-toggle="'collapse-' + prop.hop" class="m-1 bg-primary">Toggle Headers</b-button>
          <b-collapse :id="`collapse-${prop.hop}`">
            <b-card title="Header Details">
              <h3>Header Details</h3>
              <div v-for="(headerItem, headerKey) in prop.headers" :key="headerItem.server">
                <pre class="wrap-it"><small>{{ headerKey.toUpperCase() }}</small>: {{ headerItem }}</pre>
              </div>
            </b-card>
          </b-collapse>
        </div>
      </div>
    </div>
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

  finalRedirectUrl: string = '';
  fields: any = [
    {
      key: 'status_code.code',
      label: 'Status Code',
    },
    {
      key: 'status_code.phrase',
      label: 'Status Message',
    },
    {
      key: 'scheme',
      label: 'Scheme',
    },
    {
      key: 'host',
      label: 'Host',
    },
    {
      key: 'path',
      label: 'Path',
    },
  ];
  finalUrl() {
    if (this.propData.length > 0) {
      this.finalRedirectUrl = this.propData[this.propData.length - 1].url;
    } else {
      this.finalRedirectUrl = '';
    }
  }

  rowClass(item: any, type: string) {
    if (!item || type !== 'row') {
      return;
    }
    if (item.scheme !== 'https') {
      return 'table-danger';
    } else {
      return 'table-success';
    }
  }
}
</script>

<style scoped>
.wrap-it {
  /*  pre tags horizontal scroll by default
      this overrides it so its wraps
  */
  white-space: pre-wrap;
}
</style>
