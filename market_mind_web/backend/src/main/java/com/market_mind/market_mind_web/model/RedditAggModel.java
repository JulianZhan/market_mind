package com.market_mind.market_mind_web.model;

import jakarta.persistence.*;
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
