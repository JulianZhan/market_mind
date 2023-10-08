package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.dto.PriceDTO;
import com.market_mind.market_mind_web.repository.TradesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.time.LocalDateTime;

@Service
public class TradesService {

    @Autowired
    private TradesRepository tradesRepository;
    private final int defaultTimeRange = 150;

    public List<PriceDTO> getPricePerSecond() {
        int timeRange = defaultTimeRange * 1;
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startTime = now.minusSeconds(timeRange);
        return tradesRepository.findPriceByDateRangePerSecond(startTime, now);
    }

    public List<PriceDTO> getPricePerFiveSeconds() {
        int timeRange = defaultTimeRange * 5;
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startTime = now.minusSeconds(timeRange);
        return tradesRepository.findPriceByDateRangePerFiveSeconds(startTime, now);
    }

    public List<PriceDTO> getPricePerMinute() {
        int timeRange = defaultTimeRange * 60;
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startTime = now.minusSeconds(timeRange);
        return tradesRepository.findPriceByDateRangePerMinute(startTime, now);
    }
}