<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>{{ appName }} - Password Recovery</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <p class="subheading">
                A password recovery email will be sent to the registered account
              </p>
              <v-form ref="form" v-model="valid" lazy-validation @keyup.enter="submit" @submit.prevent="">
                <v-text-field
                  v-model="username"
                  v-validate="'required'"
                  label="Username"
                  type="text"
                  prepend-icon="person"
                  data-vv-name="username"
                  :error-messages="errors.collect('username')"
                  required
                  @keyup.enter="submit"
                />
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn @click="cancel">
                Cancel
              </v-btn>
              <v-btn :disabled="!valid" @click.prevent="submit">
                Recover Password
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { appName } from '@/env';
import { dispatchPasswordRecovery } from '@/store/main/actions';

@Component
export default class Login extends Vue {
  public valid = true;

  public username: string = '';

  public appName = appName;

  public cancel() {
    this.$router.back();
  }

  public submit() {
    dispatchPasswordRecovery(this.$store, { username: this.username });
  }
}
</script>

<style></style>
