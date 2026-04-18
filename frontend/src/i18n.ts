import { browser } from '$app/environment';
import { addMessages, init, getLocaleFromNavigator } from 'svelte-i18n';
import en from '$lib/locales/en.json';
import zh from '$lib/locales/zh.json';

addMessages('en', en);
addMessages('zh', zh);

init({
  fallbackLocale: 'en',
  initialLocale: browser ? (getLocaleFromNavigator() ?? 'en') : 'en',
});