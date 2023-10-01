package com.market_mind.market_mind_web.model;

import jakarta.persistence.*;
import java.time.LocalDate;

@Table(name = "alpha_vantage_agg")
@Entity
public class AlphaVantageAggModel {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "date_recorded")
    private LocalDate dateRecorded;

    @Column(name = "avg_score")
    private Double avgScore;

    @Column(name = "max_score")
    private Double maxScore;

    @Column(name = "min_score")
    private Double minScore;

    @Column(name = "std_score")
    private Double stdScore;

    // Getters
    public Long getId() {
        return id;
    }

    public LocalDate getDateRecorded() {
        return dateRecorded;
    }

    public Double getAvgScore() {
        return avgScore;
    }

    public Double getMaxScore() {
        return maxScore;
    }

    public Double getMinScore() {
        return minScore;
    }

    public Double getStdScore() {
        return stdScore;
    }

}
