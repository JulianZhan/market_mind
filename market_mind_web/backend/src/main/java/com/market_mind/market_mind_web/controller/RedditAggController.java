package com.market_mind.market_mind_web.controller;

import com.market_mind.market_mind_web.service.RedditAggService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.List;
import java.util.Map;
import java.time.LocalDate;

@RestController
@RequestMapping("/api/v1/redditagg")
public class RedditAggController {

    private static final Logger LOGGER = LogManager.getLogger(RedditAggController.class);

    @Autowired
    private RedditAggService redditAggService;

    @GetMapping("/date-range")
    public List<Map<String, Object>> getRecordWithinDateRange(@RequestParam LocalDate startDate,
            @RequestParam LocalDate endDate) {
        LOGGER.info(
                "API call: /api/v1/redditagg/date-range, startDate: %s, endDate: %s, return type: List<Map<String, Object>>",
                startDate, endDate);
        return redditAggService.getTransformedRecordWithinDateRange(startDate, endDate);
    }
}
