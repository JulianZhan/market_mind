package com.market_mind.market_mind_web.model;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;

@Table(name = "reddit_agg")
@Entity
public class RedditAggModel {
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
        BigDecimal bd = new BigDecimal(Double.toString(value));
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
