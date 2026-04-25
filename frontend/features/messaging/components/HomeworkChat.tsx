"use client";

import { useState } from "react";
import { MessageForm } from "@/features/messaging/components/MessageForm";
import type { Message } from "@/features/messaging/types/message.types";
import { useSocket } from "@/shared/lib/hooks/useSocket";
import {
  ChatSocketPayload,
  HomeworkChatProps,
} from "@/features/messaging/types/message.types";

export const HomeworkChat = ({
  initialData,
  homeworkId,
  studentId,
  accessToken,
}: HomeworkChatProps) => {
  const [messages, setMessages] = useState<Message[]>(
    initialData?.messages ?? [],
  );

  const wsBaseUrl =
    process.env.NEXT_PUBLIC_WS_BASE_URL ??
    process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/^http/, "ws");

  const socketParams = new URLSearchParams({ token: accessToken });

  if (studentId !== undefined) {
    socketParams.set("student_id", String(studentId));
  }

  const socketUrl = wsBaseUrl
    ? `${wsBaseUrl}/ws/chat/homework/${homeworkId}/?${socketParams.toString()}`
    : null;

  const appendMessage = (message: Message) => {
    setMessages((prev) => {
      if (prev.some((item) => item.id === message.id)) {
        return prev;
      }

      return [...prev, message];
    });
  };

  useSocket<ChatSocketPayload>(socketUrl, (payload) => {
    if (payload.type === "chat_message") {
      appendMessage(payload.message);
    }
  });

  return (
    <div className="space-y-6">
      <div className="space-y-6 px-1">
        {messages.length === 0 ? (
          <div className="border-primary-light text-primary-grey rounded-3xl border-2 border-dashed p-10 text-center text-sm">
            No messages in this conversation yet.
          </div>
        ) : (
          messages.map((message) => (
            <article key={message.id} className="space-y-2">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="text-primary-grey/40 text-[10px] font-black tracking-widest uppercase">
                  {message.sender.first_name} {message.sender.last_name}
                </p>

                <time className="text-primary-grey/40 text-[10px] font-medium">
                  {new Date(message.created_at).toLocaleString()}
                </time>
              </div>

              <div className="bg-primary-light/40 text-primary-dark ring-primary-light rounded-2xl p-4 text-sm leading-relaxed wrap-break-word whitespace-pre-wrap ring-1">
                {message.message_text}
              </div>
            </article>
          ))
        )}
      </div>

      <div className="border-primary-light border-t pt-5">
        <MessageForm
          homeworkId={homeworkId}
          studentId={studentId}
          onSuccess={appendMessage}
        />
      </div>
    </div>
  );
};
