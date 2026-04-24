"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import ActionButton from "@/shared/components/ActionButton";
import { routes } from "@/shared/config/routes";

const DeleteCourseButton = ({ courseId }: { courseId: number }) => {
  const router = useRouter();
  const [isPending, setIsPending] = useState(false);

  const handleDelete = async () => {
    setIsPending(true);

    try {
      const response = await fetch(`/api/courses/${courseId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete course");
      }

      router.push(routes.myCourses);
      router.refresh();
    } finally {
      setIsPending(false);
    }
  };

  return (
    <ActionButton
      label="Delete course"
      variant="danger-ghost"
      onClick={handleDelete}
      disabled={isPending}
    />
  );
};

export default DeleteCourseButton;
