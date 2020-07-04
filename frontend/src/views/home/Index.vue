<template>
  <div>
    <navbar></navbar>
    <search></search>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { appName } from '@/env';
import Navbar from '@/views/Navbar.vue';
import Search from '@/views/home/Search.vue';
@Component({
  components: { Navbar, Search },
})
export default class Index extends Vue {}
</script>

<style scoped></style>
