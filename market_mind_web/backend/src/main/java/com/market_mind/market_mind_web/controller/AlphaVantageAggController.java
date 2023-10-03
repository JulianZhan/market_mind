package com.market_mind.market_mind_web.controller;

import com.market_mind.market_mind_web.model.AlphaVantageAggModel;
import com.market_mind.market_mind_web.service.AlphaVantageAggService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.List;
import java.time.LocalDate;

@RestController
@RequestMapping("/api/v1/alphavantageagg")
public class AlphaVantageAggController {

    private static final Logger LOGGER = LogManager.getLogger(AlphaVantageAggController.class);

    @Autowired
    private AlphaVantageAggService alphaVantageAggService;

    @GetMapping("/date-range")
    public List<AlphaVantageAggModel> getRecordWithinDateRange(@RequestParam LocalDate startDate,
            @RequestParam LocalDate endDate) {
        LOGGER.info(
                String.format(
                        "API call: /api/v1/alphavantageagg/date-range, startDate: %s, endDate: %s, return type: List<AlphaVantageAggModel>",
                        startDate, endDate));
        return alphaVantageAggService.getRecordWithinDateRange(startDate, endDate);
    }
}
