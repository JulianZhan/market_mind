package com.market_mind.market_mind_web.service;

import com.market_mind.market_mind_web.model.TradesModel;
import com.market_mind.market_mind_web.repository.TradesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TradesService {

    @Autowired
    private TradesRepository tradesRepository;

    public List<TradesModel> getAllData() {
        return tradesRepository.findAll();
    }
}