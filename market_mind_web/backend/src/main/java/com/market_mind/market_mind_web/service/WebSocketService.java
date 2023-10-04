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

@Service
public class WebSocketService {

    private static final Logger LOGGER = LogManager.getLogger(WebSocketService.class);

    @Autowired
    private SimpMessagingTemplate template;

    @Autowired
    private TradesService tradesService;

    private int granularity = 5;

    @Scheduled(fixedDelay = 1000) // Every 1 second
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

        this.template.convertAndSend("/topic/trades", data);
    }

    public void setGranularity(int granularity) {
        this.granularity = granularity;
    }
}
