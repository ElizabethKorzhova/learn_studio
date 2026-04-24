import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export async function deleteMyProfile(accessToken: string): Promise<void> {
  await baseApi<void>(routes.api.profile, {
    method: "DELETE",
    accessToken,
  });
}
