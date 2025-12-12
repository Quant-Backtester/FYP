<script lang="ts">
  import { toast } from "svelte-sonner";
  import { Button } from "$lib/components/ui/button/index.js";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Checkbox } from "$lib/components/ui/checkbox/index.js";
  import { Lock, Mail, Eye, EyeOff, Loader } from "lucide-svelte";
  import {
    loginUser,
    validateEmail,
    validatePassword,
  } from "$lib/utils/auth.js";
  import { goto } from "$app/navigation";
  import type { LoginFormData } from "$lib/types/auth.js";
  import { _ } from "svelte-i18n";
  let showPassword = $state(false);
  let isLoading = $state(false);
  let email = $state("");
  let password = $state("");

  async function handleLogin() {
    if(!email || !password){
      toast.error("Please fill in all fields")
    }
    if(!validateEmail(email)){
      toast.error("Please enter a valid emmail");
    }
    if(!validatePassword(password)){
      toast.error("Password must be at least 8 characters")
    }
    isLoading = true;
    try {
      await loginUser(email, password)
    } catch(error: any){
      toast.error(error.message || "Login Failed, Please try again")
    } finally {
      isLoading = false;
    }
  }

</script>


<form onsubmit={handleLogin} class="w-full">
  <div class="flex flex-col gap-6">
    <!-- Email Field -->
    <div class="grid gap-2">
      <Label for="email">{$_("auth.login.email")}</Label>
      <div class="relative">
        <Mail class="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          id="email"
          type="email"
          placeholder="m@example.com"
          class="pl-10"
          bind:value={email}
          required
          disabled={isLoading}
        />
      </div>
    </div>

    <div class="grid gap-2">
      <div class="flex items-center">
        <Label for="password">{$_("auth.login.password")}</Label>
        <a
          href="/forget-password"
          class="ms-auto inline-block text-sm underline-offset-4 hover:underline"
          onclick={() => goto("/forget-password")}
        >
        {$_("auth.login.forgotPassword")}
        </a>
      </div>

      <div class="relative">
        <Lock class="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          id="password"
          type={showPassword ? "text" : "password"}
          class="pr-10 pl-10"
          bind:value={password}
          required
          disabled={isLoading}
        />
        <button
          type="button"
          class="absolute right-3 top-3 text-muted-foreground hover:text-foreground"
          onclick={() => (showPassword = !showPassword)}
          aria-label={showPassword ? "Hide password" : "Show password"}
        >
          {#if showPassword}
            <EyeOff class="h-4 w-4" />
          {:else}
            <Eye class="h-4 w-4" />
          {/if}
        </button>
      </div>
    </div>

    <Button type="submit" disabled={isLoading} class="w-full">
      {#if isLoading}
        <Loader class="mr-2 h-4 w-4 animate-spin" />
        {$_("auth.login.logging_in")}
      {:else}
        {$_("auth.login.login")}
      {/if}
    </Button>
  </div>
</form>