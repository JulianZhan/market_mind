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

/**
 * The @RestController annotation is a convenience annotation that is itself
 * annotated with @Controller and @ResponseBody.
 * 
 * The @Controller annotation is used to mark a class as Spring MVC Controller.
 * The @ResponseBody annotation is used to indicate a method return value should
 * be bound to the web response body.
 * 
 * The @RequestMapping annotation is used to map class to an api endpoint.
 * 
 */
@RestController
@RequestMapping("/api/v1/redditagg")
public class RedditAggController {

    private static final Logger LOGGER = LogManager.getLogger(RedditAggController.class);

    /**
     * The @Autowired annotation can be used to inject bean dependencies.
     * It inject RedditAggService bean here for further use.
     */
    @Autowired
    private RedditAggService redditAggService;

    /**
     * This method is used to handle api calls to
     * /api/v1/redditagg/date-range.
     * It simply returns data from getTransformedRecordWithinDateRange method in
     * RedditAggService.
     * 
     * 
     * @param startDate LocalDate
     * @param endDate   LocalDate
     * @return List<Map<String, Object>>
     */
    @GetMapping("/date-range")
    public List<Map<String, Object>> getRecordWithinDateRange(@RequestParam LocalDate startDate,
            @RequestParam LocalDate endDate) {
        LOGGER.info(
                String.format(
                        "API call: /api/v1/redditagg/date-range, startDate: %s, endDate: %s, return type: List<Map<String, Object>>",
                        startDate, endDate));
        return redditAggService.getTransformedRecordWithinDateRange(startDate, endDate);
    }
}
