package com.market_mind.market_mind_web.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * The @Table annotation is used to specify the database table to be used for
 * mapping.
 * The @Entity annotation is used to specify that the class is an entity and is
 * mapped to a database table.
 */
@Table(name = "trades")
@Entity
public class TradesModel {
    /**
     * This class is used to represent the data from the trades table
     */
    // The @Id annotation is used to specify the primary key of an entity.
    // The @GeneratedValue annotation is used to specify how the primary key should
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "trade_timestamp")
    private LocalDateTime tradeTimestamp;

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

    public LocalDateTime getTradeTimestamp() {
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
