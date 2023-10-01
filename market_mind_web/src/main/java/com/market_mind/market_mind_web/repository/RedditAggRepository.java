package com.market_mind.market_mind_web.repository;

import com.market_mind.market_mind_web.model.RedditAggModel;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RedditAggRepository extends JpaRepository<RedditAggModel, Long> {
}
