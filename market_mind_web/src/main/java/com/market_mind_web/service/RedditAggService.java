package com.market_mind_web.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.time.LocalDate;
import com.market_mind_web.model.RedditAgg;
import com.market_mind_web.repository.RedditAggRepository;

@Service
public class RedditAggService {

    @Autowired
    private RedditAggRepository repository;

    public List<RedditAgg> getRecordsByDate(LocalDate date) {
        return repository.findByDateRecorded(date);
    }

    // Any other service methods...
}
