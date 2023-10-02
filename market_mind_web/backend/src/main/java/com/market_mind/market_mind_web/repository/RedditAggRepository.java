package com.market_mind.market_mind_web.repository;

import com.market_mind.market_mind_web.model.RedditAggModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface RedditAggRepository extends JpaRepository<RedditAggModel, Long> {

    @Query("SELECT r FROM RedditAggModel r WHERE r.dateRecorded BETWEEN :startDate AND :endDate")
    List<RedditAggModel> findDataByDateRange(@Param("startDate") LocalDate startDate,
            @Param("endDate") LocalDate endDate);

    @Query("SELECT r FROM RedditAggModel r ORDER BY r.dateRecorded DESC LIMIT 12")
    List<RedditAggModel> findTopByOrderByDateRecordedDesc();

}
