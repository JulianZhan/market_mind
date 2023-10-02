package com.market_mind.market_mind_web.controller;

import com.market_mind.market_mind_web.model.AlphaVantageAggModel;
import com.market_mind.market_mind_web.service.AlphaVantageAggService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.time.LocalDate;

@RestController
@CrossOrigin(origins = "#{@frontendOrigin}")
@RequestMapping("/api/v1/alphavantageagg")
public class AlphaVantageAggController {

    @Autowired
    private AlphaVantageAggService alphaVantageAggService;

    @GetMapping("/date-range")
    public List<AlphaVantageAggModel> getRecordWithinDateRange(@RequestParam LocalDate startDate,
            @RequestParam LocalDate endDate) {
        return alphaVantageAggService.getRecordWithinDateRange(startDate, endDate);
    }
}
