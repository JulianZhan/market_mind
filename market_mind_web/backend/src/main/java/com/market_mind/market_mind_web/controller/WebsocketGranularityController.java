package com.market_mind.market_mind_web.controller;

import com.market_mind.market_mind_web.service.WebSocketService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

@RestController
@RequestMapping("/api/v1/granularity")
public class WebsocketGranularityController {

    private static final Logger LOGGER = LogManager.getLogger(WebsocketGranularityController.class);

    @Autowired
    private WebSocketService webSocketService;

    @PostMapping
    public ResponseEntity<Void> setGranularity(@RequestParam int granularity) {
        webSocketService.setGranularity(granularity);
        LOGGER.info("API call: /api/v1/granularity, granularity: %d", granularity);
        return ResponseEntity.ok().build();
    }
}
