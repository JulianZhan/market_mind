package com.market_mind.market_mind_web.model;

import jakarta.persistence.*;
import java.time.LocalDate;

@Table(name = "trades")
@Entity
public class TradesModel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "trade_timestamp")
    private LocalDate tradeTimestamp;

    @Column(name = "symbol")
    private String symbol;

    @Column(name = "price")
    private Double price;

    @Column(name = "volume")
    private Double volume;

    // Getters
    public Long getId() {
        return id;
    }

    public LocalDate getTradeTimestamp() {
        return tradeTimestamp;
    }

    public String getSymbol() {
        return symbol;
    }

    public Double getPrice() {
        return price;
    }

    public Double getVolume() {
        return volume;
    }
}
