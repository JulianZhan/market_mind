package com.market_mind.market_mind_web.repository;

import com.market_mind.market_mind_web.dto.PriceDTO;
import com.market_mind.market_mind_web.model.TradesModel;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;

public interface TradesRepository extends JpaRepository<TradesModel, Long> {

        @Query("SELECT new com.market_mind.market_mind_web.dto.PriceDTO(AVG(t.price) as price, MIN(t.tradeTimestamp) as tradeTimestamp) FROM TradesModel t WHERE t.tradeTimestamp BETWEEN :startDate AND :endDate GROUP BY FUNCTION('HOUR', t.tradeTimestamp), FUNCTION('MINUTE', t.tradeTimestamp), FUNCTION('SECOND', t.tradeTimestamp)")
        List<PriceDTO> findPriceByDateRangePerSecond(@Param("startDate") LocalDateTime startDate,
                        @Param("endDate") LocalDateTime endDate);

        @Query("SELECT new com.market_mind.market_mind_web.dto.PriceDTO(AVG(t.price) as price, MIN(t.tradeTimestamp) as tradeTimestamp) FROM TradesModel t WHERE t.tradeTimestamp BETWEEN :startDate AND :endDate GROUP BY FUNCTION('HOUR', t.tradeTimestamp), FUNCTION('MINUTE', t.tradeTimestamp), FUNCTION('SECOND', t.tradeTimestamp) / 5")
        List<PriceDTO> findPriceByDateRangePerFiveSeconds(@Param("startDate") LocalDateTime startDate,
                        @Param("endDate") LocalDateTime endDate);

        @Query("SELECT new com.market_mind.market_mind_web.dto.PriceDTO(AVG(t.price) as price, MIN(t.tradeTimestamp) as tradeTimestamp) FROM TradesModel t WHERE t.tradeTimestamp BETWEEN :startDate AND :endDate GROUP BY FUNCTION('HOUR', t.tradeTimestamp), FUNCTION('MINUTE', t.tradeTimestamp)")
        List<PriceDTO> findPriceByDateRangePerMinute(@Param("startDate") LocalDateTime startDate,
                        @Param("endDate") LocalDateTime endDate);

}
