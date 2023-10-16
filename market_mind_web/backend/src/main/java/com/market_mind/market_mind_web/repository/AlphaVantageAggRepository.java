package com.market_mind.market_mind_web.repository;

import com.market_mind.market_mind_web.model.AlphaVantageAggModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

/**
 * Make AlphaVantageAggModel a repository, which extends JpaRepository
 * for CRUD operations with methods provided by Spring Data JPA.
 */
public interface AlphaVantageAggRepository extends JpaRepository<AlphaVantageAggModel, Long> {
    /**
     * This class is used to retrieve data from the database, serving as a
     * repository.
     */

    /**
     * This method is used to retrieve data from the database by date range.
     * Use @Query to write a custom query to retrieve data from the database.
     * 
     * @param startDate LocalDate
     * @param endDate   LocalDate
     * @return List<AlphaVantageAggModel>
     */
    @Query("SELECT a FROM AlphaVantageAggModel a WHERE a.dateRecorded BETWEEN :startDate AND :endDate")
    List<AlphaVantageAggModel> findDataByDateRange(@Param("startDate") LocalDate startDate,
            @Param("endDate") LocalDate endDate);

}
