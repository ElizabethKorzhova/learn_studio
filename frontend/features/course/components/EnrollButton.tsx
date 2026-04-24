"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import ActionButton from "@/shared/components/ActionButton";

const EnrollButton = ({ courseId }: { courseId: number }) => {
  const router = useRouter();
  const [isPending, setIsPending] = useState(false);

  const handleEnroll = async () => {
    setIsPending(true);

    try {
      const response = await fetch("/api/enrollments", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ course: courseId }),
      });

      if (!response.ok) {
        throw new Error("Failed to enroll");
      }

      router.refresh();
    } finally {
      setIsPending(false);
    }
  };

  return (
    <ActionButton
      label="Enroll course"
      onClick={handleEnroll}
      disabled={isPending}
    />
  );
};

export default EnrollButton;
