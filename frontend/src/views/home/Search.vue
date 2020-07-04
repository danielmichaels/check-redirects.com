<template>
  <div id="search">
    <div class="container">
      <h1>
        Check Redirects
        <span><h5>Get redirect routes at your fingertips</h5></span>
      </h1>
    </div>
    <!-- Start Search Form  -->
    <div class="container">
      <b-form v-if="show" @submit="onSubmit" @reset="resetData">
        <b-form-group id="search-input-group" label="search" label-for="search-input" description="Enter the URL here">
          <b-form-input
            id="search-input"
            v-model="form.url"
            type="search"
            required
            placeholder="Enter URL To Check"
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </div>
    <results :prop-data="responseData"></results>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import { apiUrl } from '@/env';
import { Component, Vue } from 'vue-property-decorator';
import Results from '@/views/home/Results.vue';

@Component({
  components: { Results },
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
    let res = this;
    axios
      .post(`${apiUrl}/api/v1/redirect/checker/`, {
        url: this.form.url,
      })
      .then((resp) => {
        this.responseData = resp.data;
        this.clearForm();
      })
      .catch((error) => {
        res.responseData = error;
      });
  }
}
</script>

<style scoped></style>
