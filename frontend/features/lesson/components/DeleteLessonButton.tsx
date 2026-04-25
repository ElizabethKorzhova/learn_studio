"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import ActionButton from "@/shared/components/ActionButton";
import { routes } from "@/shared/config/routes";

const DeleteLessonButton = ({
  lessonId,
  courseId,
}: {
  lessonId: number;
  courseId: number;
}) => {
  const router = useRouter();
  const [isPending, setIsPending] = useState(false);

  const handleDelete = async () => {
    setIsPending(true);

    try {
      const response = await fetch(
        `${routes.api.lesson(String(lessonId))}?course_id=${courseId}`,
        {
          method: "DELETE",
        },
      );

      if (!response.ok) {
        throw new Error("Failed to delete lesson");
      }

      router.push(routes.course(String(courseId)));
      router.refresh();
    } finally {
      setIsPending(false);
    }
  };

  return (
    <ActionButton
      label="Delete lesson"
      variant="danger-ghost"
      onClick={handleDelete}
      disabled={isPending}
    />
  );
};

export default DeleteLessonButton;
