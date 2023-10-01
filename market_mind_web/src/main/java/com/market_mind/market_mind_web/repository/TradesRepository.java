package com.market_mind.market_mind_web.repository;

import com.market_mind.market_mind_web.model.TradesModel;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TradesRepository extends JpaRepository<TradesModel, Long> {
}
