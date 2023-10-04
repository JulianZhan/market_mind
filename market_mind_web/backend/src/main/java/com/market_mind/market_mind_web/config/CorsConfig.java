package com.market_mind.market_mind_web.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**") // Match all endpoints
                .allowedOrigins("*") // Allow any origin
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS"); // Allow specific HTTP methods
    };
}
