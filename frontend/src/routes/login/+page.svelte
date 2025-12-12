<script lang="ts">
  import LoginForm from "$lib/components/auth/LoginForm.svelte";
  import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card/index.js";
  import { Separator } from "$lib/components/ui/separator/index.js";
  import * as Alert from "$lib/components/ui/alert/index.js";
  import AlertCircleIcon from "@lucide/svelte/icons/alert-circle";
  import { goto } from "$app/navigation";
  import { _ } from "svelte-i18n";
</script>

<div
  class="min-h-screen flex items-center justify-center bg-linear-to-br from-gray-50 to-gray-100 p-4"
>
  <div class="w-full max-w-md">
    <Card class="border shadow-lg">
      <CardHeader class="text-center">
        <CardTitle class="text-2xl font-bold tracking-tight">
          {$_("auth.login.description")}
        </CardTitle>
        <CardDescription class="text-muted-foreground">
          {$_("auth.login.title")}
        </CardDescription>
      </CardHeader>
      <CardContent class="space-y-6">
        <LoginForm />

        <Separator class="my-6" />

        <div class="text-center space-y-4">
          <p class="text-sm text-muted-foreground">
            {$_("auth.login.noAccount")}
            <button
              onclick={() => goto("/signup")}
              class="ml-2 font-medium text-primary hover:text-primary/80 underline-offset-2 hover:underline transition-colors"
            >
              {$_("auth.login.signup")}
            </button>
          </p>
          <p class="text-xs text-muted-foreground">
            {$_("continue")}
            <a href="/terms" class="text-primary hover:underline ml-1"
              >{$_("term")}</a
            >
            {$_("and")}
            <a href="/privacy" class="text-primary hover:underline ml-1"
              >{$_("privacy")}</a
            >
          </p>
        </div>
      </CardContent>
    </Card>
  </div>
</div>
