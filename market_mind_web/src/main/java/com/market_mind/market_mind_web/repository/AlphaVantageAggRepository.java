package com.market_mind.market_mind_web.repository;

import com.market_mind.market_mind_web.model.AlphaVantageAggModel;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AlphaVantageAggRepository extends JpaRepository<AlphaVantageAggModel, Long> {
}