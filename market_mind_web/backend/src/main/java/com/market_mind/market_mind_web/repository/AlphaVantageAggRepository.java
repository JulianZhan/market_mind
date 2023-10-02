package com.market_mind.market_mind_web.repository;

import com.market_mind.market_mind_web.model.AlphaVantageAggModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface AlphaVantageAggRepository extends JpaRepository<AlphaVantageAggModel, Long> {

    // Retrieve the data between a date range
    @Query("SELECT a FROM AlphaVantageAggModel a WHERE a.dateRecorded BETWEEN :startDate AND :endDate")
    List<AlphaVantageAggModel> findDataByDateRange(@Param("startDate") LocalDate startDate,
            @Param("endDate") LocalDate endDate);

}
