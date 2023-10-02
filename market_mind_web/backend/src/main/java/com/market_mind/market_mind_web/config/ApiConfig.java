package com.market_mind.market_mind_web.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ApiConfig {

    @Value("${backend.host}")
    private String backendHost;

    @Value("${frontend.host}")
    private String frontendHost;

    @Bean
    public String backendOrigin() {
        return backendHost + ":8080";
    }

    @Bean
    public String frontendOrigin() {
        return frontendHost + ":3000";
    }
}
