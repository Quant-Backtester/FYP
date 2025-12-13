import z from 'zod'

export const loginSchema = z.object({
  email: z.email().min(1),
  password: z.string().min(8).max(40),
})


