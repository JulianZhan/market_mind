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

    public List<PriceAndVolumeDTO> getPriceAndVolumeWithinDateRange(LocalDate startDate, LocalDate endDate) {
        LocalDateTime startDateTime = startDate.atStartOfDay();
        LocalDateTime endDateTime = endDate.atTime(23, 59, 59, 999999999);

        return tradesRepository.findPriceAndVolumeByDateRange(startDateTime, endDateTime);
    }
}