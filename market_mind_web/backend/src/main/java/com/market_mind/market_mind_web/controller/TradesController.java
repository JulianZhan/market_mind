package com.market_mind.market_mind_web.controller;

import com.market_mind.market_mind_web.service.TradesService;
import com.market_mind.market_mind_web.dto.PriceAndVolumeDTO;
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

    @GetMapping("/date-range")
    public List<PriceAndVolumeDTO> getPriceAndVolumeWithinDateRange(@RequestParam LocalDate startDate,
            @RequestParam LocalDate endDate) {
        return tradesService.getPriceAndVolumeWithinDateRange(startDate, endDate);
    }

    @GetMapping("/last-30-minutes")
    public List<PriceAndVolumeDTO> getLast30MinutesPriceAndVolume() {
        return tradesService.getLast30MinutesPriceAndVolume();
    }
}