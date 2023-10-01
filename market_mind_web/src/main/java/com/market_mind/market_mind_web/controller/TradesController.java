package com.market_mind.market_mind_web.controller;

import com.market_mind.market_mind_web.model.TradesModel;
import com.market_mind.market_mind_web.service.TradesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.time.LocalDate;

@RestController
@RequestMapping("/api/v1/trades")
public class TradesController {

    @Autowired
    private TradesService tradesService;

    @GetMapping
    public List<TradesModel> getAllData() {
        return tradesService.getAllData();
    }

    @GetMapping("/start-date")
    public List<Double> getRecordAfterDate(@RequestParam LocalDate date) {
        return tradesService.getRecordAfterDate(date);
    }
}