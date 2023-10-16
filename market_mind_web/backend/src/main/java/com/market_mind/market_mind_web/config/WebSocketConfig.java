package com.market_mind.market_mind_web.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * The WebSocketMessageBrokerConfigurer interface provides methods to configure
 * the WebSocket connection.
 * The @EnableScheduling annotation enables the scheduling of tasks to produce
 * messages, allowing the @Scheduled annotation to be used in beans.
 * The @EnableWebSocketMessageBroker annotation enables WebSocket message, it
 * signals that the application will act as a WebSocket server and will handle
 * messaging through this protocol.
 */
@Configuration
@EnableScheduling
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    /**
     * This class is used to configure the WebSocket connection.
     * Use constructor injection to inject the frontendOrigin bean from
     * ApiConfig.java to this class.
     */

    private final String frontendOrigin;

    public WebSocketConfig(String frontendOrigin) {
        this.frontendOrigin = frontendOrigin;
    }

    /**
     * Override the configureMessageBroker method to configure the message broker.
     * enableSimpleBroker method sets the destination prefix to /topic.
     * setApplicationDestinationPrefixes method sets the destination prefix to /app.
     * for messages sent from clients to the message broker, the endpoint will be
     * prefixed with /app.
     */
    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        config.enableSimpleBroker("/topic");
        config.setApplicationDestinationPrefixes("/app");
    }

    /**
     * Override the registerStompEndpoints method to register the endpoint.
     * Set the allowed origins to the frontendOrigin.
     * Use withSockJS method to support communication with clients through browser
     */
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/api/v1/websocket-endpoint").setAllowedOrigins(frontendOrigin).withSockJS();

    }
}
