package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.model.AlphaVantageAggModel;
import com.market_mind.market_mind_web.repository.AlphaVantageAggRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.List;
import java.time.LocalDate;

/**
 * The @Service annotation indicates that an annotated class is a service class,
 * which is used to implement business logic.
 */
@Service
public class AlphaVantageAggService {
    /**
     * This class is used to implement business logic over
     * AlphaVantageAggRepository.
     */

    private static final Logger LOGGER = LogManager.getLogger(AlphaVantageAggService.class);

    /**
     * The @Autowired annotation can be used to inject bean dependencies.
     * It inject AlphaVantageAggRepository bean here for further use.
     */
    @Autowired
    private AlphaVantageAggRepository alphaVantageAggRepository;

    /**
     * This method is used to get data from AlphaVantageAggRepository.
     * It simply returns data from findDataByDateRange method in
     * AlphaVantageAggRepository.
     * 
     * @param startDate LocalDate
     * @param endDate   LocalDate
     * @return List<AlphaVantageAggModel>
     */
    public List<AlphaVantageAggModel> getRecordWithinDateRange(LocalDate startDate, LocalDate endDate) {
        LOGGER.info(String.format("Get data from AlphaVantageAggRepository, startDate: %s, endDate: %s", startDate,
                endDate));
        return alphaVantageAggRepository.findDataByDateRange(startDate, endDate);
    }

}