<script lang="ts">
  import SignupForm from './SignupForm.svelte';
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card/index.js';
  import { Separator } from '$lib/components/ui/separator/index.js';
  import { Alert, AlertDescription } from '$lib/components/ui/alert/index.js';
  import { goto } from '$app/navigation';
  import { _ } from 'svelte-i18n';


</script>

<div class="min-h-screen flex items-center justify-center bg-linear-to-br from-gray-50 to-gray-100 p-4">
  <div class="w-full max-w-md">
    <Card class="border shadow-lg">
      <CardHeader class="text-center">
        <CardTitle class="text-2xl font-bold tracking-tight">
          Create an Account
        </CardTitle>
        <CardDescription class="text-muted-foreground">
          Fill in your details to get started
        </CardDescription>
      </CardHeader>
      <CardContent class="space-y-6">

        <SignupForm />

        <Separator class="my-6" />

        <div class="text-center space-y-4">
          <p class="text-sm text-muted-foreground">
            Already have an account?
            <button
              onclick={()=> { goto("/login")}}
              class="ml-2 font-medium text-primary hover:text-primary/80 underline-offset-2 hover:underline transition-colors"
            >
              Login here
            </button>
          </p>
          <p class="text-xs text-muted-foreground">
            By creating an account, you agree to our
            <a href="/terms" class="text-primary hover:underline ml-1">{$_("term")}</a>
            and
            <a href="/privacy" class="text-primary hover:underline ml-1">{$_("privacy")}</a>
          </p>
        </div>
      </CardContent>
    </Card>
  </div>
</div>