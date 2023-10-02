package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.dto.PriceAndVolumeDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;
import org.springframework.scheduling.annotation.Scheduled;

import java.util.List;

@Service
public class WebSocketService {

    @Autowired
    private SimpMessagingTemplate template;

    @Autowired
    private TradesService tradesService;

    @Scheduled(fixedDelay = 5000) // Every 5 seconds
    public void sendLast30MinutesPriceAndVolume() {
        List<PriceAndVolumeDTO> data = tradesService.getLast30MinutesPriceAndVolume();
        this.template.convertAndSend("/topic/last-30-minutes", data);
    }
}
