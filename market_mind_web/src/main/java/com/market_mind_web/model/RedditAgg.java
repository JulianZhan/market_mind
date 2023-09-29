package com.market_mind_web.model;

import javax.persistence.Entity;
import javax.persistence.Table;
import javax.persistence.Id;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Column;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "reddit_emotions")
public class RedditAgg {

    @Column(name = "id")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "date_recorded")
    private LocalDate dateRecorded;
    @Column(name = "emotion_name")
    private String emotionName;
    @Column(name = "avg_score")
    private Double avgScore;

}
