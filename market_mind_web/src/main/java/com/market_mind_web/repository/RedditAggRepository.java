package com.market_mind_web.repository;

import com.market_mind_web.model.RedditAgg;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.time.LocalDate;

public interface RedditAggRepository extends JpaRepository<RedditAgg, Long> {
    List<RedditAgg> findByDateRecorded(LocalDate date);
}
