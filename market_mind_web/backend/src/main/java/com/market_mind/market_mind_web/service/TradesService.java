package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.dto.PriceAndVolumeDTO;
import com.market_mind.market_mind_web.repository.TradesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Service
public class TradesService {

    @Autowired
    private TradesRepository tradesRepository;
    private int defaultTimeRange = 300;

    public List<PriceAndVolumeDTO> getPriceAndVolumePerSecond() {
        defaultTimeRange = defaultTimeRange * 1;
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startTime = now.minusSeconds(defaultTimeRange);
        return tradesRepository.findPriceAndVolumeByDateRangePerSecond(startTime, now);
    }

    public List<PriceAndVolumeDTO> getPriceAndVolumePerFiveSeconds() {
        defaultTimeRange = defaultTimeRange * 5;
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startTime = now.minusSeconds(defaultTimeRange);
        return tradesRepository.findPriceAndVolumeByDateRangePerFiveSeconds(startTime, now);
    }

    public List<PriceAndVolumeDTO> getPriceAndVolumePerMinute() {
        defaultTimeRange = defaultTimeRange * 60;
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startTime = now.minusSeconds(defaultTimeRange);
        return tradesRepository.findPriceAndVolumeByDateRangePerMinute(startTime, now);
    }
}