package com.market_mind.market_mind_web.repository;

import com.market_mind.market_mind_web.dto.PriceAndVolumeDTO;
import com.market_mind.market_mind_web.model.TradesModel;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;

public interface TradesRepository extends JpaRepository<TradesModel, Long> {

    @Query("SELECT new com.market_mind.market_mind_web.dto.PriceAndVolumeDTO(AVG(t.price) as avgPrice, SUM(t.volume) as totalVolume, MIN(t.tradeTimestamp) as minTimestamp) FROM TradesModel t WHERE t.tradeTimestamp BETWEEN :startDate AND :endDate GROUP BY FUNCTION('HOUR', t.tradeTimestamp), FUNCTION('MINUTE', t.tradeTimestamp), FUNCTION('SECOND', t.tradeTimestamp)")
    List<PriceAndVolumeDTO> findPriceAndVolumeByDateRangePerSecond(@Param("startDate") LocalDateTime startDate,
            @Param("endDate") LocalDateTime endDate);

    @Query("SELECT new com.market_mind.market_mind_web.dto.PriceAndVolumeDTO(AVG(t.price) as avgPrice, SUM(t.volume) as totalVolume, MIN(t.tradeTimestamp) as minTimestamp) FROM TradesModel t WHERE t.tradeTimestamp BETWEEN :startDate AND :endDate GROUP BY FUNCTION('HOUR', t.tradeTimestamp), FUNCTION('MINUTE', t.tradeTimestamp), FUNCTION('SECOND', t.tradeTimestamp) DIV 5")
    List<PriceAndVolumeDTO> findPriceAndVolumeByDateRangePerFiveSeconds(@Param("startDate") LocalDateTime startDate,
            @Param("endDate") LocalDateTime endDate);

    @Query("SELECT new com.market_mind.market_mind_web.dto.PriceAndVolumeDTO(AVG(t.price) as avgPrice, SUM(t.volume) as totalVolume, MIN(t.tradeTimestamp) as minTimestamp) FROM TradesModel t WHERE t.tradeTimestamp BETWEEN :startDate AND :endDate GROUP BY FUNCTION('HOUR', t.tradeTimestamp), FUNCTION('MINUTE', t.tradeTimestamp)")
    List<PriceAndVolumeDTO> findPriceAndVolumeByDateRangePerMinute(@Param("startDate") LocalDateTime startDate,
            @Param("endDate") LocalDateTime endDate);

}
