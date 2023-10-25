package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.model.RedditAggModel;
import com.market_mind.market_mind_web.repository.RedditAggRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The @Service annotation indicates that an annotated class is a service class,
 * which is used to implement business logic.
 */
@Service
public class RedditAggService {
    /**
     * This class is used to implement business logic over
     * RedditAggRepository.
     */

    private static final Logger LOGGER = LogManager.getLogger(RedditAggService.class);

    /**
     * The @Autowired annotation can be used to inject bean dependencies.
     * It inject RedditAggRepository bean here for further use.
     */
    @Autowired
    private RedditAggRepository redditAggRepository;

    /**
     * This method is used to get data from RedditAggRepository.
     * It implements transformation on the data from RedditAggRepository.
     * 
     * @param startDate LocalDate
     * @param endDate   LocalDate
     * @return List<Map<String, Object>>
     */
    public List<Map<String, Object>> getTransformedRecordWithinDateRange(LocalDate startDate, LocalDate endDate) {
        List<RedditAggModel> originalData = redditAggRepository.findDataByDateRange(startDate, endDate);

        /**
         * Transform data from RedditAggRepository.
         * It first init a LinkedHashMap to store transformed data.
         * LinkedHashMap is used here to preserve key and value and the order of
         * insertion.
         */
        Map<LocalDate, Map<String, Object>> transformedData = new LinkedHashMap<>();
        for (RedditAggModel item : originalData) {
            /**
             * For each item in originalData, computeIfAbsent is used to check if the key
             * dateRecorded exists in transformedData. If not, it will create a new
             * LinkedHashMap to store the data for this key/ dateRecorded.
             * Later, it will put the data for this item into the LinkedHashMap.
             */
            transformedData
                    .computeIfAbsent(item.getDateRecorded(), date -> new LinkedHashMap<String, Object>())
                    .put(item.getEmotionName(), item.getAvgScore());
        }

        /**
         * For each item in transformedData(date, map), put the date into the map as a
         * key-value pair.
         */
        transformedData.forEach((date, map) -> map.put("dateRecorded", date.toString()));

        LOGGER.info(String.format("Get transformed data from RedditAggRepository, startDate: %s, endDate: %s",
                startDate, endDate));

        /**
         * Return the values of transformedData as a List.
         */
        return new ArrayList<>(transformedData.values());
    }

}
