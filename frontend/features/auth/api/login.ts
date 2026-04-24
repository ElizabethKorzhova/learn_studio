import {
  LoginDataType,
  AuthRouteSuccess,
} from "@/features/auth/types/auth.types";
import baseApi from "@/shared/lib/api/baseApi";
import { routes } from "@/shared/config/routes";

export const login = (payload: LoginDataType): Promise<AuthRouteSuccess> => {
  return baseApi<AuthRouteSuccess>(routes.api.login, {
    method: "POST",
    body: payload,
    baseUrl: "",
  }) as Promise<AuthRouteSuccess>;
};
