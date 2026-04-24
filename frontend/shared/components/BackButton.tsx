"use client";

import ActionButton from "@/shared/components/ActionButton";
import { useRouter } from "next/navigation";

const BackButton = () => {
  const router = useRouter();
  return (
    <div className="flex justify-start">
      <ActionButton
        label="← Back"
        variant="xs-ghost"
        onClick={() => router.back()}
      />
    </div>
  );
};

export default BackButton;
