<template>
  <div id="search">
    <div class="container text-center">
      <h1>
        Check Redirects
        <b-card-sub-title><h5>Get redirect routes at your fingertips</h5></b-card-sub-title>
      </h1>
    </div>
    <!-- Start Search Form  -->
    <div class="container text-center">
      <b-form v-if="show" class="container" @submit="onSubmit" @reset="resetData">
        <h3>Search</h3>
        <b-form-group id="search-input-group" label-for="search-input">
          <b-form-input
            id="search-input"
            v-model="form.url"
            type="search"
            required
            placeholder="Enter URL To Check"
          ></b-form-input>
        </b-form-group>
        <div>
          <b-button class="mr-1" size="lg" type="submit" variant="primary">Submit</b-button>
          <b-button size="lg" type="reset" variant="danger">Reset</b-button>
        </div>
      </b-form>
    </div>
    <div v-if="responseData.length !== 0">
      <div v-if="responseData[0].error">
        <results-error :prop-data="responseData"></results-error>
      </div>
      <div v-else>
        <results-success :prop-data="responseData"></results-success>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import { apiUrl } from '@/env';
import { Component, Vue } from 'vue-property-decorator';
import ResultsSuccess from '@/views/home/ResultsSuccess.vue';
import ResultsError from '@/views/home/ResultsError.vue';

@Component({
  components: { ResultsSuccess, ResultsError },
})
export default class Search extends Vue {
  show = true;
  public url = '';
  public responseData = [];

  form = {
    url: '',
  };

  public clearForm() {
    this.form.url = '';
    this.$nextTick(() => {
      this.show = true;
    });
  }

  public resetData() {
    this.responseData = [];
    this.$forceUpdate();
  }

  public onSubmit(evt) {
    evt.preventDefault();
    this.resetData();
    let res = this;
    axios
      .post(`${apiUrl}/api/v1/redirect/checker`, {
        url: this.form.url,
      })
      .then((resp) => {
        this.responseData = resp.data;
        this.clearForm();
      })
      .catch((error) => {
        // push this to notification instead
        console.log(error);
      });
  }
}
</script>

<style scoped></style>
