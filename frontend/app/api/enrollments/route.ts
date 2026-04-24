import { NextResponse } from "next/server";

import { createEnrollment } from "@/features/course/api/createEnrollment";
import { getSession } from "@/shared/lib/auth/getSession";

export const POST = async (request: Request) => {
  const session = await getSession();

  if (!session) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  try {
    const body = await request.json();
    const enrollment = await createEnrollment(session.accessToken, body);

    return NextResponse.json(enrollment, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { message: error instanceof Error ? error.message : "Failed to enroll" },
      { status: 400 },
    );
  }
};
