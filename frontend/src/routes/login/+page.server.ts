import type { PageServerLoad, Actions } from "./$types.js";
import { fail } from "@sveltejs/kit";

import { loginSchema } from "$lib/schemas/LoginSchema.js";

export const load = async () => {
};

export const actions: Actions = {
  login: async ({ request }) => {
    const data = await request.formData();
    console.log(data)

  },
};