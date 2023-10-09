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
@Table(name = "reddit_agg")
@Entity
public class RedditAggModel {
    /**
     * This class is used to represent the data from the reddit_agg table
     */
    // The @Id annotation is used to specify the primary key of an entity.
    // The @GeneratedValue annotation is used to specify how the primary key should
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "date_recorded")
    private LocalDate dateRecorded;

    @Column(name = "emotion_name")
    private String emotionName;

    @Column(name = "avg_score")
    private Double avgScore;

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

    public String getEmotionName() {
        return emotionName;
    }

    public Double getAvgScore() {
        return avgScore;
    }

}
