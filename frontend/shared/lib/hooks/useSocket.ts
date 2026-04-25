import { useEffect, useRef } from "react";

export const useSocket = <T>(
  url: string | null,
  onMessage: (data: T) => void,
) => {
  const socketRef = useRef<WebSocket | null>(null);
  const onMessageRef = useRef(onMessage);

  useEffect(() => {
    onMessageRef.current = onMessage;
  }, [onMessage]);

  useEffect(() => {
    if (!url) return;

    const socket = new WebSocket(url);
    socket.onopen = () => console.log("WS OPEN", url);
    socket.onmessage = (event) => {
      console.log("WS MESSAGE RAW", event.data);
      const data = JSON.parse(event.data);
      onMessageRef.current(data);
    };
    socket.onclose = (event) =>
      console.log("WS CLOSE", event.code, event.reason);
    socket.onerror = (event) => console.log("WS ERROR", event);

    socketRef.current = socket;

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessageRef.current(data);
    };

    return () => {
      socket.close();
      socketRef.current = null;
    };
  }, [url]);
};
