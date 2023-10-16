package com.market_mind.market_mind_web.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * The WebMvcConfigurer interface provides methods to customize the Java-based
 * configuration for Spring MVC.
 * This is a hook provided by Spring MVC to configure CORS.
 */
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    /**
     * This class is used to configure the allowed origins from the frontend.
     * Use constructor injection to inject the frontendOrigin bean from
     * ApiConfig.java to this class.
     */

    private final String frontendOrigin;

    public CorsConfig(String frontendOrigin) {
        this.frontendOrigin = frontendOrigin;
    }

    // Override the addCorsMappings method to configure the allowed origins.
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**") // Match all endpoints
                .allowedOrigins(frontendOrigin)
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true);
    };
}
