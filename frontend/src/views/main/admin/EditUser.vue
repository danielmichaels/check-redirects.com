<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">
          Edit User
        </div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">
              Username
            </div>
            <div v-if="user" class="title primary--text text--darken-2">
              {{ user.email }}
            </div>
            <div v-else class="title primary--text text--darken-2">
              -----
            </div>
          </div>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field v-model="fullName" label="Full Name" required />
            <v-text-field
              v-model="email"
              v-validate="'required|email'"
              label="E-mail"
              type="email"
              data-vv-name="email"
              :error-messages="errors.collect('email')"
              required
            />
            <div class="subheading secondary--text text--lighten-2">
              User is superuser <span v-if="isSuperuser">(currently is a superuser)</span
              ><span v-else>(currently is not a superuser)</span>
            </div>
            <v-checkbox v-model="isSuperuser" label="Is Superuser" />
            <div class="subheading secondary--text text--lighten-2">
              User is active <span v-if="isActive">(currently active)</span><span v-else>(currently not active)</span>
            </div>
            <v-checkbox v-model="isActive" label="Is Active" />
            <v-layout align-center>
              <v-flex shrink>
                <v-checkbox v-model="setPassword" class="mr-2" />
              </v-flex>
              <v-flex>
                <v-text-field
                  ref="password"
                  v-model="password1"
                  v-validate="{ required: setPassword }"
                  :disabled="!setPassword"
                  type="password"
                  label="Set Password"
                  data-vv-name="password"
                  data-vv-delay="100"
                  :error-messages="errors.first('password')"
                />
                <v-text-field
                  v-show="setPassword"
                  v-model="password2"
                  v-validate="{ required: setPassword, confirmed: 'password' }"
                  type="password"
                  label="Confirm Password"
                  data-vv-name="password_confirmation"
                  data-vv-delay="100"
                  data-vv-as="password"
                  :error-messages="errors.first('password_confirmation')"
                />
              </v-flex>
            </v-layout>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="cancel">
          Cancel
        </v-btn>
        <v-btn @click="reset">
          Reset
        </v-btn>
        <v-btn :disabled="!valid" @click="submit">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IUserProfileUpdate } from '@/interfaces';
import { dispatchGetUsers, dispatchUpdateUser } from '@/store/admin/actions';
import { readAdminOneUser } from '@/store/admin/getters';

@Component
export default class EditUser extends Vue {
  public valid = true;

  public fullName: string = '';

  public email: string = '';

  public isActive: boolean = true;

  public isSuperuser: boolean = false;

  public setPassword = false;

  public password1: string = '';

  public password2: string = '';

  public async mounted() {
    await dispatchGetUsers(this.$store);
    this.reset();
  }

  public reset() {
    this.setPassword = false;
    this.password1 = '';
    this.password2 = '';
    this.$validator.reset();
    if (this.user) {
      this.fullName = this.user.full_name;
      this.email = this.user.email;
      this.isActive = this.user.is_active;
      this.isSuperuser = this.user.is_superuser;
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedProfile: IUserProfileUpdate = {};
      if (this.fullName) {
        updatedProfile.full_name = this.fullName;
      }
      if (this.email) {
        updatedProfile.email = this.email;
      }
      updatedProfile.is_active = this.isActive;
      updatedProfile.is_superuser = this.isSuperuser;
      if (this.setPassword) {
        updatedProfile.password = this.password1;
      }
      await dispatchUpdateUser(this.$store, { id: this.user!.id, user: updatedProfile });
      this.$router.push('/main/admin/users');
    }
  }

  get user() {
    return readAdminOneUser(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
