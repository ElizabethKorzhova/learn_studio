import type { CurrentUser } from "@/features/auth/types/auth.types";
import type { UpdateMyProfilePayload } from "@/features/profile/types/profile.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export async function updateMyProfile(
  accessToken: string,
  payload: UpdateMyProfilePayload,
): Promise<CurrentUser> {
  return (await baseApi<CurrentUser>(routes.api.profile, {
    method: "PATCH",
    accessToken,
    body: payload,
  })) as CurrentUser;
}
