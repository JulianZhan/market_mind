import SockJS from "sockjs-client";
import { Client } from "@stomp/stompjs";
import CONFIG from "../config";
import { utcToZonedTime } from "date-fns-tz";
const API_BASE_URL = CONFIG.API_BASE_URL;

export const initiateWebSocketConnection = (onMessageReceived, onConnected) => {
  /**
   * This function initiates a websocket connection to the server.
   * @Param {Function} onMessageReceived - A callback function that is executed
   * when a message is received from the server.
   * @Return {Object} - A stomp client object.
   */

  /**
   * Create a new socket object and connect to the websocket endpoint.
   * SockJS is a browser JavaScript library that provides a WebSocket-like object,
   * SockJS can enable browsers to use the WebSocket API
   */
  const socket = new SockJS(`${API_BASE_URL}/websocket-endpoint`);

  /**
   * Create a new stomp client object and subscribe to the /topic/trades endpoint.
   * STOMP stands for Simple Text Orientated Messaging Protocol.
   * It is a simple protocol that allows clients to send and receive messages on top of websockets.
   */
  const stompClient = new Client({
    // webSocketFactory is a function that returns a WebSocket object.
    webSocketFactory: () => socket,
    /**
     * onConnect is a callback function that is executed when the client connects to the server.
     * when the client connects to the server, it subscribes to the /topic/trades endpoint.
     * then, it transforms the data received from the server to the user's timezone.
     */
    onConnect: () => {
      onConnected();
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
        /**
         * For each message received, we execute the onMessageReceived callback function.
         * This function will be like setData in useState, it will update the state of the component.
         */
        onMessageReceived(adjustedData);
      });
    },
  });
  stompClient.activate();

  return stompClient;
};

export const updateGranularityOnServer = async (granularity) => {
  /**
   * This function updates the granularity on the server.
   * @Param {String} granularity - The granularity to be updated.
   * @Return {Void} - Nothing.
   */
  await fetch(`${API_BASE_URL}/granularity`, {
    method: "POST",
    // URLSearchParams is a built in class that allows us to construct a query string.
    body: new URLSearchParams({ granularity }),
  });
};
