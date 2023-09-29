package com.market_mind_web.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import java.util.List;
import java.time.LocalDate;
import com.market_mind_web.model.RedditAgg;
import com.market_mind_web.service.RedditAggService;

@RestController
@RequestMapping("/emotion-records")
public class RedditAggController {

    @Autowired
    private RedditAggService service;

    @GetMapping("/by-date")
    public List<RedditAgg> getRecordsByDate(@RequestParam LocalDate date) {
        return service.getRecordsByDate(date);
    }

}
