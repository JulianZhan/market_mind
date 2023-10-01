package com.market_mind.market_mind_web.controller;

import com.market_mind.market_mind_web.model.RedditAggModel;
import com.market_mind.market_mind_web.service.RedditAggService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/redditagg")
public class RedditAggController {

    @Autowired
    private RedditAggService redditAggService;

    @GetMapping
    public List<RedditAggModel> getAllData() {
        return redditAggService.getAllData();
    }

    // Add more endpoints as required
}
