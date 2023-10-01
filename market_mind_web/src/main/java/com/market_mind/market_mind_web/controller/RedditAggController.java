package com.market_mind.market_mind_web.controller;

import com.market_mind.market_mind_web.model.RedditAggModel;
import com.market_mind.market_mind_web.service.RedditAggService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.time.LocalDate;

@RestController
@RequestMapping("/api/v1/redditagg")
public class RedditAggController {

    @Autowired
    private RedditAggService redditAggService;

    @GetMapping
    public List<RedditAggModel> getAllData() {
        return redditAggService.getAllData();
    }

    @GetMapping("/date-range")
    public List<RedditAggModel> getRecordWithinDateRange(@RequestParam LocalDate startDate,
            @RequestParam LocalDate endDate) {
        return redditAggService.getRecordWithinDateRange(startDate, endDate);
    }

    @GetMapping("/recent")
    public RedditAggModel getMostRecentRecord() {
        return redditAggService.getMostRecentRecord();
    }
}
