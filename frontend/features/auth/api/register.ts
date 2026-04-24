import type {
  AuthRouteSuccess,
  RegisterDataType,
} from "@/features/auth/types/auth.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const register = async (
  payload: RegisterDataType,
): Promise<AuthRouteSuccess> => {
  return (await baseApi<AuthRouteSuccess>(routes.api.register, {
    method: "POST",
    body: payload,
    baseUrl: "",
  })) as AuthRouteSuccess;
};
