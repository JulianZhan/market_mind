package com.market_mind.market_mind_web.model;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;

/**
 * The @Table annotation is used to specify the database table to be used for
 * mapping.
 * The @Entity annotation is used to specify that the class is an entity and is
 * mapped to a database table.
 */
@Table(name = "alpha_vantage_agg")
@Entity
public class AlphaVantageAggModel {
    /**
     * This class is used to represent the data from the alpha_vantage_agg table
     */

    // The @Id annotation is used to specify the primary key of an entity.
    // The @GeneratedValue annotation is used to specify how the primary key should
    // be generated.
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

    // Helper method to round values to two decimal places
    private Double round(Double value) {
        if (value == null) {
            return null;
        }
        // The BigDecimal class provides operations for arithmetic, scale
        BigDecimal bd = new BigDecimal(Double.toString(value));
        // setScale() method rounds the value to the given number of digits after the
        // decimal point.
        bd = bd.setScale(2, RoundingMode.HALF_UP);
        return bd.doubleValue();
    }

    @PostLoad
    public void onPostLoad() {
        this.avgScore = round(this.avgScore);
    }

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
