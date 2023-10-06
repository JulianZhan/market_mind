import SockJS from "sockjs-client";
import { Client } from "@stomp/stompjs";
import CONFIG from "../config";
const API_BASE_URL = CONFIG.API_BASE_URL;

export const initiateWebSocketConnection = (onMessageReceived) => {
  const socket = new SockJS(`${API_BASE_URL}/websocket-endpoint`);

  const getUserTimezone = () => {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
  };

  const adjustToTaiwanTime = (timestamp) => {
    const userTimezone = getUserTimezone();
    const date = new Date(timestamp);
    const userLocalDate = new Date(
      date.toLocaleString("en-US", { timeZone: userTimezone })
    );
    return userLocalDate.getTime(); // Returns timestamp in milliseconds
  };

  const stompClient = new Client({
    webSocketFactory: () => socket,
    onConnect: () => {
      stompClient.subscribe("/topic/trades", (message) => {
        const rawData = JSON.parse(message.body);
        rawData.tradeTimestamp = adjustToTaiwanTime(rawData.tradeTimestamp);
        onMessageReceived(rawData);
      });
    },
  });
  stompClient.activate();

  return stompClient;
};

export const updateGranularityOnServer = async (granularity) => {
  await fetch(`${API_BASE_URL}/granularity`, {
    method: "POST",
    body: new URLSearchParams({ granularity }),
  });
};
