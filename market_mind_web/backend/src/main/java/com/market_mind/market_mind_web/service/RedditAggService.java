package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.model.RedditAggModel;
import com.market_mind.market_mind_web.repository.RedditAggRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Service
public class RedditAggService {

    @Autowired
    private RedditAggRepository redditAggRepository;

    public List<Map<String, Object>> getTransformedRecordWithinDateRange(LocalDate startDate, LocalDate endDate) {
        List<RedditAggModel> originalData = redditAggRepository.findDataByDateRange(startDate, endDate);

        Map<LocalDate, Map<String, Object>> transformedData = new LinkedHashMap<>();
        for (RedditAggModel item : originalData) {
            transformedData
                    .computeIfAbsent(item.getDateRecorded(), date -> new LinkedHashMap<String, Object>())
                    .put(item.getEmotionName(), item.getAvgScore());
        }

        transformedData.forEach((date, map) -> map.put("dateRecorded", date.toString()));

        return new ArrayList<>(transformedData.values());
    }

    public List<Map<String, Object>> getTransformedMostRecentRecord() {
        List<RedditAggModel> originalData = redditAggRepository.findTopByOrderByDateRecordedDesc();

        Map<LocalDate, Map<String, Object>> transformedData = new LinkedHashMap<>();
        for (RedditAggModel item : originalData) {
            transformedData
                    .computeIfAbsent(item.getDateRecorded(), date -> new LinkedHashMap<String, Object>())
                    .put(item.getEmotionName(), item.getAvgScore());
        }

        transformedData.forEach((date, map) -> map.put("dateRecorded", date.toString()));

        return new ArrayList<>(transformedData.values());
    }

}
