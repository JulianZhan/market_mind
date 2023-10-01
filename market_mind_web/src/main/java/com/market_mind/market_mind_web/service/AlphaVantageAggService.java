package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.model.AlphaVantageAggModel;
import com.market_mind.market_mind_web.repository.AlphaVantageAggRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.time.LocalDate;

@Service
public class AlphaVantageAggService {

    @Autowired
    private AlphaVantageAggRepository alphaVantageAggRepository;

    public List<AlphaVantageAggModel> getAllData() {
        return alphaVantageAggRepository.findAll();
    }

    public List<AlphaVantageAggModel> getRecordWithinDateRange(LocalDate startDate, LocalDate endDate) {
        return alphaVantageAggRepository.findDataByDateRange(startDate, endDate);
    }

    public AlphaVantageAggModel getMostRecentRecord() {
        return alphaVantageAggRepository.findTopByOrderByDateRecordedDesc();
    }
}