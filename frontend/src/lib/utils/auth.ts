import { toast } from 'svelte-sonner';
import type { AuthResponse } from '$lib/types/auth.js';

export const loginUser = async (email: string, password: string): Promise<AuthResponse> => {
  await new Promise(resolve => setTimeout(resolve, 1000));


  if (email === 'demo@example.com' && password === 'password123') {
    return {
      success: true,
      user: {
        id: '1',
        name: 'Demo User',
        email: email
      }
    };
  }

  return {
    success: false,
    message: 'Invalid email or password'
  };
};

export const signupUser = async (
  name: string,
  email: string,
  password: string
): Promise<AuthResponse> => {
  await new Promise(resolve => setTimeout(resolve, 1000));

  if (!name || !email || !password) {
    return {
      success: false,
      message: 'Please fill in all required fields'
    };
  }

  if (password.length < 6) {
    return {
      success: false,
      message: 'Password must be at least 6 characters'
    };
  }

  // Mock successful signup
  return {
    success: true,
    user: {
      id: '2',
      name,
      email
    }
  };
};

export const resetPassword = async (email: string): Promise<AuthResponse> => {

  // replace with the real api call
  await new Promise(resolve => setTimeout(resolve, 1000));

  if (!email) {
    return {
      success: false,
      message: 'Please enter your email address'
    };
  }

  return {
    success: true,
    message: 'Password reset instructions sent to your email'
  };
};

// Form validation
export const validateEmail = (email: string): string | null => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email) return 'Email is required';
  if (!emailRegex.test(email)) return 'Please enter a valid email';
  return null;
};

export const validatePassword = (password: string): string | null => {
  if (!password) return 'Password is required';
  if (password.length < 8) return 'Password must be at least 6 characters';
  return null;
};