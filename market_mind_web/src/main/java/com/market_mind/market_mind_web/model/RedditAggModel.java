package com.market_mind.market_mind_web.model;

import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import jakarta.persistence.*;
import java.util.Date;

@Table(name = "reddit_agg")
@Entity
public class RedditAggModel {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "date_recorded")
    private Date dateRecorded;

    @Column(name = "emotion_name")
    private String emotionName;

    @Column(name = "avg_score")
    private Double avgScore;

    // Getters
    public Long getId() {
        return id;
    }

    public Date getDateRecorded() {
        return dateRecorded;
    }

    public String getEmotionName() {
        return emotionName;
    }

    public Double getAvgScore() {
        return avgScore;
    }

}
