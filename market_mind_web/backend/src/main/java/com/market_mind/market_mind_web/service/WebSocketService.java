package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.dto.PriceDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;
import org.springframework.scheduling.annotation.Scheduled;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.Collections;
import java.util.List;

/**
 * The @Service annotation indicates that an annotated class is a service class,
 * which is used to implement business logic.
 */
@Service
public class WebSocketService {
    /**
     * This class uses methods from TradesService and provides a layer of
     * abstraction to build a WebSocket service.
     */

    private static final Logger LOGGER = LogManager.getLogger(WebSocketService.class);

    /**
     * The @Autowired annotation use to inject bean dependencies.
     */
    @Autowired
    private SimpMessagingTemplate template;

    @Autowired
    private TradesService tradesService;

    private int granularity = 5;

    /**
     * The @Scheduled annotation can be added to a method along with trigger
     * metadata. This method will be executed on a schedule.
     * 
     * @Scheduled(fixedDelay = 1000) means the method will be executed every 1000
     *                       milliseconds.
     */
    @Scheduled(fixedDelay = 1000)
    public void sendPriceAndVolumeBasedOnGranularity() {
        List<PriceDTO> data;

        switch (granularity) {
            case 1:
                data = tradesService.getPricePerSecond();
                break;
            case 5:
                data = tradesService.getPricePerFiveSeconds();
                break;
            case 60:
                data = tradesService.getPricePerMinute();
                break;
            default:
                data = Collections.emptyList();
                LOGGER.error(String.format("Invalid granularity: ", granularity));

        }

        // send data to WebSocket
        this.template.convertAndSend("/topic/trades", data);
    }

    /**
     * This method is used to set granularity.
     * Provide a entry point for websocketGranularityController.
     * 
     * @param granularity int
     */
    public void setGranularity(int granularity) {
        this.granularity = granularity;
    }
}
