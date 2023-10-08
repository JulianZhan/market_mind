package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.model.AlphaVantageAggModel;
import com.market_mind.market_mind_web.repository.AlphaVantageAggRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.List;
import java.time.LocalDate;

@Service
public class AlphaVantageAggService {

    private static final Logger LOGGER = LogManager.getLogger(AlphaVantageAggService.class);

    @Autowired
    private AlphaVantageAggRepository alphaVantageAggRepository;

    public List<AlphaVantageAggModel> getRecordWithinDateRange(LocalDate startDate, LocalDate endDate) {
        LOGGER.info(String.format("Get data from AlphaVantageAggRepository, startDate: %s, endDate: %s", startDate,
                endDate));
        return alphaVantageAggRepository.findDataByDateRange(startDate, endDate);
    }

}