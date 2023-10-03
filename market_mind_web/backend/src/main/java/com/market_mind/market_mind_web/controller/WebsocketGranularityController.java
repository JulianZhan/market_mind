package com.market_mind.market_mind_web.controller;

import com.market_mind.market_mind_web.service.WebSocketService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@RestController
@RequestMapping("/api/v1/granularity")
public class WebsocketGranularityController {

    @Autowired
    private WebSocketService webSocketService;

    @PostMapping
    public ResponseEntity<Void> setGranularity(@RequestParam int granularity) {
        webSocketService.setGranularity(granularity);
        return ResponseEntity.ok().build();
    }
}
