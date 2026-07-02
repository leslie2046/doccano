<template>
  <div v-if="social.length" class="social-login">
    <div class="social-login__separator" aria-hidden="true">
      <span class="social-login__line"></span>
      <span class="social-login__label">{{ $t('user.socialLoginSeparator') }}</span>
      <span class="social-login__line"></span>
    </div>

    <v-btn
      v-for="item in social"
      :key="item.id"
      block
      elevation="0"
      outlined
      :href="item.href"
      class="social-login__button"
    >
      {{ $t('user.socialLogin', { provider: item.provider }) }}
    </v-btn>
  </div>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import Vue from 'vue'

export default Vue.extend({
  props: {
    fetchSocialLink: {
      type: Function as PropType<() => Promise<any>>,
      required: true
    }
  },
  data() {
    return {
      social: [] as Array<{ id: string; provider: string; href: string }>
    }
  },
  async mounted() {
    try {
      const response = await this.fetchSocialLink()
      this.social = Object.entries(response)
        .map(([key, value]: any) => ({
          id: key,
          value
        }))
        .filter((item) => !!(item.value?.href || item.value?.authorize_url))
        .map((item: any) => ({
          id: item.id,
          provider: item.value.label || item.id,
          href:
            item.value.href ||
            `${item.value.authorize_url}&redirect_uri=${location.origin}${item.value.redirect_path}`
        }))
    } catch (e) {
      console.error(e)
    }
  }
})
</script>

<style scoped>
.social-login {
  margin-top: 18px;
}

.social-login__separator {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.social-login__line {
  flex: 1;
  height: 1px;
  background: #d9dfeb;
}

.social-login__label {
  color: #8a93a5;
  font-size: 12px;
  line-height: 1;
  white-space: nowrap;
}

.social-login__button {
  min-height: 46px;
  border: 1px solid #d6dde8 !important;
  background: #ffffff !important;
  color: #2f3747 !important;
  box-shadow: none !important;
  letter-spacing: 0.02em;
  text-transform: none;
}

.social-login__button:hover {
  border-color: #b9c5d8 !important;
  background: #f8fafc !important;
}
</style>
