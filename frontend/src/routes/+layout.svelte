<script lang="ts">
  import { Loader } from "svelte-sonner";
  import { waitLocale } from "svelte-i18n";
  import "./layout.css";
  import "../i18n.ts"



  let { children } = $props();
</script>

{#await waitLocale()}
<Loader visible={true}/>
{:then}
  {@render children()}
{/await}
