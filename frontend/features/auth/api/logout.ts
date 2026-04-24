import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const logout = async (): Promise<{ ok: true }> => {
  await baseApi<void>(routes.api.logout, {
    method: "POST",
    baseUrl: "",
  });
  return { ok: true };
};
