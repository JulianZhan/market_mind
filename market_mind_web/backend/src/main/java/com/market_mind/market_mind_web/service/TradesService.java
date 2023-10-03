package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.dto.PriceAndVolumeDTO;
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

    public List<PriceAndVolumeDTO> getPriceAndVolumePerSecond() {
        int timeRange = defaultTimeRange * 1;
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startTime = now.minusSeconds(timeRange);
        return tradesRepository.findPriceAndVolumeByDateRangePerSecond(startTime, now);
    }

    public List<PriceAndVolumeDTO> getPriceAndVolumePerFiveSeconds() {
        int timeRange = defaultTimeRange * 5;
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startTime = now.minusSeconds(timeRange);
        return tradesRepository.findPriceAndVolumeByDateRangePerFiveSeconds(startTime, now);
    }

    public List<PriceAndVolumeDTO> getPriceAndVolumePerMinute() {
        int timeRange = defaultTimeRange * 60;
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startTime = now.minusSeconds(timeRange);
        return tradesRepository.findPriceAndVolumeByDateRangePerMinute(startTime, now);
    }
}