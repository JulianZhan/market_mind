package com.market_mind.market_mind_web.dto;

import java.time.LocalDateTime;

public class PriceAndVolumeDTO {
    private Double price;
    private Double volume;
    private LocalDateTime tradeTimestamp;

    public PriceAndVolumeDTO(Double price, Double volume, LocalDateTime tradeTimestamp) {
        this.price = price;
        this.volume = volume;
        this.tradeTimestamp = tradeTimestamp;
    }

    public Double getPrice() {
        return price;
    }

    public Double getVolume() {
        return volume;
    }

    public LocalDateTime getTradeTimestamp() {
        return tradeTimestamp;
    }
}
