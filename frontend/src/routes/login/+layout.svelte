<script>
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let { children } = $props()

  onMount(() => {
    const token = localStorage.getItem('auth_token');
    if(token){
      goto("/home")
    }
  });
</script>

{@render children()}