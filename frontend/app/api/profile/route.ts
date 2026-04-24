import { NextResponse } from "next/server";
import { getSession } from "@/shared/lib/auth/getSession";
import { updateMyProfile } from "@/features/profile/api/updateMyProfile";
import { deleteMyProfile } from "@/features/profile/api/deleteMyProfile";

export const PATCH = async (request: Request) => {
  try {
    const session = await getSession();

    if (!session?.accessToken) {
      return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
    }

    const payload = await request.json();
    const profile = await updateMyProfile(session.accessToken, payload);

    return NextResponse.json(profile);
  } catch (error) {
    return NextResponse.json(
      {
        message:
          error instanceof Error ? error.message : "Failed to update profile",
      },
      { status: 400 },
    );
  }
};

export const DELETE = async () => {
  const session = await getSession();

  if (!session?.accessToken) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  await deleteMyProfile(session.accessToken);

  return NextResponse.json({ success: true });
};
