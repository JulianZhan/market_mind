package com.market_mind.market_mind_web.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.context.annotation.Bean;

@Configuration
public class CorsConfig {

    private final String frontendOrigin;

    public CorsConfig(String frontendOrigin) {
        this.frontendOrigin = frontendOrigin;
    }

    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/**")
                        .allowedOrigins(frontendOrigin)
                        .allowedMethods("GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS");
            }
        };
    }
}
