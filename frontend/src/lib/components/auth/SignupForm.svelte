<script lang="ts">
  import * as Form from '$lib/components/ui/form/index.js';
  import { Button } from '$lib/components/ui/button/index.js';
  import { Input } from '$lib/components/ui/input/index.js';
  import { Label } from '$lib/components/ui/label/index.js';
  import { Checkbox } from '$lib/components/ui/checkbox/index.js';
  import { Lock, Mail, User, Eye, EyeOff, Loader } from 'lucide-svelte';
  import { signupUser,  validateEmail, validatePassword } from '$lib/utils/auth.ts';
  import { goto } from '$app/navigation';
  import { toast } from 'svelte-sonner';
  import { createForm } from 'svelte-forms-lib';
  import type { SignupFormData } from '$lib/types/auth.js';
  import { _ } from "svelte/i18n"


  let showPassword = false;
  let showConfirmPassword = false;
  let isLoading = false;

  // Additional validations
  const validateName = (name: string): string | null => {
    if (!name) return 'Name is required';
    if (name.length < 2) return 'Name must be at least 2 characters';
    return null;
  };

  const validateConfirmPassword = (confirmPassword: string, values: SignupFormData): string | null => {
    if (!confirmPassword) return 'Please confirm your password';
    if (confirmPassword !== values.password) return 'Passwords do not match';
    return null;
  };

  const validateTerms = (agreeToTerms: boolean): string | null => {
    if (!agreeToTerms) return 'You must agree to the terms';
    return null;
  };


<Form {form} {handleSubmit} class="space-y-4">
  <!-- Name Field -->
  <div class="space-y-2">
    <Label for="name" class="text-sm font-medium">
      Full Name
    </Label>
    <div class="relative">
      <User class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      <Input
        id="name"
        type="text"
        name="name"
        placeholder="John Doe"
        value={$form.name}
        on:input={(e) => handleChange('name', e.target.value)}
        class="pl-10"
        required
      />
    </div>
    {#if $errors.name}
      <p class="text-sm text-destructive">{@html $errors.name}</p>
    {/if}
  </div>

  <!-- Email Field -->
  <div class="space-y-2">
    <Label for="email" class="text-sm font-medium">
      Email Address
    </Label>
    <div class="relative">
      <Mail class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      <Input
        id="email"
        type="email"
        name="email"
        placeholder="you@example.com"
        value={$form.email}
        on:input={(e) => handleChange('email', e.target.value)}
        class="pl-10"
        required
      />
    </div>
    {#if $errors.email}
      <p class="text-sm text-destructive">{@html $errors.email}</p>
    {/if}
  </div>

  <!-- Password Field -->
  <div class="space-y-2">
    <Label for="password" class="text-sm font-medium">
      Password
    </Label>
    <div class="relative">
      <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      <Input
        id="password"
        bind:value={$form.password}
        oninput={(e) => handleChange('password', e.target.value)}
        type={showPassword ? 'text' : 'password'}
        placeholder="Create a password"
        class="pl-10 pr-10"
        required
      />
      <button
        type="button"
        on:click={() => showPassword = !showPassword}
        class="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground"
        aria-label={showPassword ? 'Hide password' : 'Show password'}
      >
        {#if showPassword}
          <EyeOff class="h-4 w-4" />
        {:else}
          <Eye class="h-4 w-4" />
        {/if}
      </button>
    </div>
    {#if $errors.password}
      <p class="text-sm text-destructive">{@html $errors.password}</p>
    {/if}
  </div>

  <!-- Confirm Password Field -->
  <div class="space-y-2">
    <Label for="confirmPassword" class="text-sm font-medium">
      Confirm Password
    </Label>
    <div class="relative">
      <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      <Input
        id="confirmPassword"
        bind:value={$form.confirmPassword}
        on:input={(e) => handleChange('confirmPassword', e.target.value)}
        type={showConfirmPassword ? 'text' : 'password'}
        placeholder="Confirm your password"
        class="pl-10 pr-10"
        required
      />
      <button
        type="button"
        on:click={() => showConfirmPassword = !showConfirmPassword}
        class="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground"
        aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
      >
        {#if showConfirmPassword}
          <EyeOff class="h-4 w-4" />
        {:else}
          <Eye class="h-4 w-4" />
        {/if}
      </button>
    </div>
    {#if $errors.confirmPassword}
      <p class="text-sm text-destructive">{@html $errors.confirmPassword}</p>
    {/if}
  </div>

  <!-- Terms Agreement -->
  <div class="space-y-2">
    <div class="flex items-start space-x-2">
      <Checkbox
        id="agreeToTerms"
        checked={$form.agreeToTerms}
        on:change={() => handleChange('agreeToTerms', !$form.agreeToTerms)}
        class="mt-1"
      />
      <div class="grid gap-1.5 leading-none">
        <Label for="agreeToTerms" class="text-sm font-medium leading-none cursor-pointer">
          I agree to the terms and conditions
        </Label>
        <p class="text-sm text-muted-foreground">
          By creating an account, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
    {#if $errors.agreeToTerms}
      <p class="text-sm text-destructive">{@html $errors.agreeToTerms}</p>
    {/if}
  </div>

  <!-- Submit Button -->
  <Button
    type="submit"
    class="w-full"
    disabled={isLoading}
  >
    {#if isLoading}
      <Loader class="mr-2 h-4 w-4 animate-spin" />
      Creating account...
    {:else}
      Create Account
    {/if}
  </Button>
</Form>