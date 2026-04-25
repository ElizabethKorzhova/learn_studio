import { NextResponse } from "next/server";
import {
  deleteHomework,
  updateHomework,
} from "@/features/homework/api/manageHomework";
import { getSession } from "@/shared/lib/auth/getSession";

type RouteProps = {
  params: Promise<{ id: string }>;
};

export const PATCH = async (request: Request, { params }: RouteProps) => {
  const session = await getSession();

  if (!session) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const body = await request.json();

  try {
    const homework = await updateHomework(session.accessToken, id, body);

    return NextResponse.json(homework, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      {
        message:
          error instanceof Error ? error.message : "Failed to update homework",
      },
      { status: 400 },
    );
  }
};

export const DELETE = async (_request: Request, { params }: RouteProps) => {
  const session = await getSession();

  if (!session) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;

  try {
    await deleteHomework(session.accessToken, id);

    return new NextResponse(null, { status: 204 });
  } catch (error) {
    return NextResponse.json(
      {
        message:
          error instanceof Error ? error.message : "Failed to delete homework",
      },
      { status: 400 },
    );
  }
};
