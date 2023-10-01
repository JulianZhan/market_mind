package com.market_mind.market_mind_web.repository;

import com.market_mind.market_mind_web.model.TradesModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface TradesRepository extends JpaRepository<TradesModel, Long> {

    @Query("SELECT t.price FROM TradesModel t WHERE t.tradeTimestamp >= :startDate")
    List<Double> findTradesAfterDate(@Param("startDate") LocalDate startDate);
}
