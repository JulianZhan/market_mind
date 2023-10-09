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

/**
 * The @RestController annotation is a convenience annotation that is itself
 * annotated with @Controller and @ResponseBody.
 * 
 * The @Controller annotation is used to mark a class as Spring MVC Controller.
 * The @ResponseBody annotation is used to indicate a method return value should
 * be bound to the web response body.
 * 
 * The @RequestMapping annotation is used to map class to an api endpoint.
 */
@RestController
@RequestMapping("/api/v1/granularity")
public class WebsocketGranularityController {

    private static final Logger LOGGER = LogManager.getLogger(WebsocketGranularityController.class);

    /**
     * The @Autowired annotation can be used to inject bean dependencies.
     * It inject WebSocketService bean here for further use.
     */
    @Autowired
    private WebSocketService webSocketService;

    /**
     * This method is used to handle api calls to
     * /api/v1/granularity.
     * It will set granularity in WebSocketService.
     * Then, it will return a ResponseEntity without body, except for a 200 OK
     * status.
     * 
     * @param granularity int
     * @return ResponseEntity<Void>
     */
    @PostMapping
    public ResponseEntity<Void> setGranularity(@RequestParam int granularity) {
        webSocketService.setGranularity(granularity);
        LOGGER.info(String.format("API call: /api/v1/granularity, granularity: %d", granularity));
        return ResponseEntity.ok().build();
    }
}
