package com.market_mind.market_mind_web.repository;

import com.market_mind.market_mind_web.dto.PriceAndVolumeDTO;
import com.market_mind.market_mind_web.model.TradesModel;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface TradesRepository extends JpaRepository<TradesModel, Long> {

    @Query("SELECT new com.market_mind.market_mind_web.dto.PriceAndVolumeDTO(t.price, t.volume) FROM TradesModel t WHERE t.tradeTimestamp BETWEEN :startDate AND :endDate")
    List<PriceAndVolumeDTO> findPriceAndVolumeByDateRange(@Param("startDate") LocalDate startDate,
            @Param("endDate") LocalDate endDate);
}
