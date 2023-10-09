import SockJS from "sockjs-client";
import { Client } from "@stomp/stompjs";
import CONFIG from "../config";
import { utcToZonedTime } from "date-fns-tz";
const API_BASE_URL = CONFIG.API_BASE_URL;

export const initiateWebSocketConnection = (onMessageReceived) => {
  /**
   * This function initiates a websocket connection to the server.
   * @Param {Function} onMessageReceived - A callback function that is executed
   * when a message is received from the server.
   * @Return {Object} - A stomp client object.
   */

  // Instantiate a SockJS object with the websocket endpoint.
  const socket = new SockJS(`${API_BASE_URL}/websocket-endpoint`);

  const stompClient = new Client({
    webSocketFactory: () => socket,
    onConnect: () => {
      stompClient.subscribe("/topic/trades", (message) => {
        const rawData = JSON.parse(message.body);
        const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        const adjustedData = rawData.map((trade) => ({
          ...trade,
          tradeTimestamp: utcToZonedTime(
            trade.tradeTimestamp + "Z",
            userTimeZone
          ),
        }));
        onMessageReceived(adjustedData);
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
