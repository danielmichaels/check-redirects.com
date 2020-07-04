<template>
  <div id="search">
    <div class="container-fluid">
      <h1>
        Check Redirects
        <span><h5>Get redirect routes at your fingertips</h5></span>
      </h1>
    </div>
    <!-- Start Search Form  -->
    <div class="container-fluid">
      <b-form v-if="show" @submit="onSubmit">
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
      <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ form }}</pre>
      </b-card>
    </div>
    <!--  End Search Form -->
    <b-card class="mt-3" header="Raw Response">
      <pre class="m-0">{{ resp }}</pre>
    </b-card>
  </div>
</template>

<script lang="js">
import axios from 'axios';
import {apiUrl} from "@/env";

export default {
  data() {
    return {
      form: {
        url: '',
      },
      show: true,
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      let res = this;
      axios.post(`${apiUrl}/api/v1/redirect/checker/`,
              {
                url: this.form.url,
              })
      .then((resp) => {
        resp.output = resp.data;
        this.clearForm();
      })
      .catch((error) => {
        res.output = error;
      });
      console.log(JSON.stringify(this.form))
    },
    clearForm() {
      this.form.url = ''
      this.$nextTick(() => {
        this.show = true
      })
    }
  }
}
</script>

<style scoped></style>
