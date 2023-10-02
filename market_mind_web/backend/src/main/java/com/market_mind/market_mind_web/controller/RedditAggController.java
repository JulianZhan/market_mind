package com.market_mind.market_mind_web.controller;

import com.market_mind.market_mind_web.service.RedditAggService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.util.Map;
import java.time.LocalDate;

@RestController
@CrossOrigin(origins = "http://localhost:3000")
@RequestMapping("/api/v1/redditagg")
public class RedditAggController {

    @Autowired
    private RedditAggService redditAggService;

    @GetMapping("/date-range")
    public List<Map<String, Object>> getRecordWithinDateRange(@RequestParam LocalDate startDate,
            @RequestParam LocalDate endDate) {
        return redditAggService.getTransformedRecordWithinDateRange(startDate, endDate);
    }

    @GetMapping("/recent")
    public Map<String, Object> getTransformedMostRecentRecord() {
        List<Map<String, Object>> list = redditAggService.getTransformedMostRecentRecord();
        return list.get(0);
    }
}
