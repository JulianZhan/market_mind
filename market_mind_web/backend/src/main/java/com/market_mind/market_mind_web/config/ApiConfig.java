package com.market_mind.market_mind_web.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

// The @Configuration annotation indicates that this is a class providing source of bean definitions.
@Configuration
public class ApiConfig {
    /**
     * This class is used to configure the origins of the backend and frontend.
     * Use Value annotation to inject the values from application.properties to the
     * beans.
     * After that, the beans can be injected into other classes.
     */

    // It reads the value of backend.host from application.properties
    @Value("${backend.host}")
    private String backendHost;

    @Value("${frontend.host}")
    private String frontendHost;

    // It creates a bean with the name backendOrigin and value backendHost + ":8080"
    @Bean
    public String backendOrigin() {
        return backendHost + ":8080";
    }

    @Bean
    public String frontendOrigin() {
        return frontendHost;
    }
}
