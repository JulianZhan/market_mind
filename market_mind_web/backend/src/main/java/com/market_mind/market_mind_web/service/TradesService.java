package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.dto.PriceDTO;
import com.market_mind.market_mind_web.repository.TradesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.time.LocalDateTime;

/**
 * The @Service annotation indicates that an annotated class is a service class,
 * which is used to implement business logic.
 */
@Service
public class TradesService {
    /**
     * This class is used to implement business logic over
     * TradesRepository.
     */

    /**
     * The @Autowired annotation use to inject bean dependencies.
     */
    @Autowired
    private TradesRepository tradesRepository;
    // init default time length for data available for display
    private final int defaultTimeRange = 100;

    /**
     * The following methods are used to get data from TradesRepository.
     * It calculates the start time based on the default time range and
     * the multiplication of granularity.
     */
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