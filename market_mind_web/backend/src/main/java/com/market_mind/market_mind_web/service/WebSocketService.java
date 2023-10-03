package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.dto.PriceAndVolumeDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;
import org.springframework.scheduling.annotation.Scheduled;

import java.util.Collections;
import java.util.List;

@Service
public class WebSocketService {

    @Autowired
    private SimpMessagingTemplate template;

    @Autowired
    private TradesService tradesService;

    private int granularity = 5;

    @Scheduled(fixedDelay = 1000) // Every 1 second
    public void sendPriceAndVolumeBasedOnGranularity() {
        List<PriceAndVolumeDTO> data;
        switch (granularity) {
            case 1:
                data = tradesService.getPriceAndVolumePerSecond();
                break;
            case 5:
                data = tradesService.getPriceAndVolumePerFiveSeconds();
                break;
            case 60:
                data = tradesService.getPriceAndVolumePerMinute();
                break;
            default:
                data = Collections.emptyList();
        }
        this.template.convertAndSend("/topic/trades", data);
    }

    public void setGranularity(int granularity) {
        this.granularity = granularity;
    }
}
