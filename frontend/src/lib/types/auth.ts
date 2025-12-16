export type LoginFormData = {
    email: string;
    password: string;
    rememberMe: boolean;
}

export type SignupFormData = {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  agreeToTerms: boolean;
}

export type AuthResponse = {
  success: boolean;
  message?: string;
  user?: {
    id: string;
    name: string;
    email: string;
  };
}

export type AuthError = {
  field?: string;
  message: string;
}