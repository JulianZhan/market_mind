package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.model.RedditAggModel;
import com.market_mind.market_mind_web.repository.RedditAggRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class RedditAggService {

    @Autowired
    private RedditAggRepository redditAggRepository;

    public List<RedditAggModel> getAllData() {
        return redditAggRepository.findAll();
    }

    public List<RedditAggModel> getRecordWithinDateRange(LocalDate startDate, LocalDate endDate) {
        return redditAggRepository.findDataByDateRange(startDate, endDate);
    }

    public RedditAggModel getMostRecentRecord() {
        return redditAggRepository.findTopByOrderByDateRecordedDesc();
    }
}
