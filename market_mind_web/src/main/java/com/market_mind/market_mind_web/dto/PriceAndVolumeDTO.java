package com.market_mind.market_mind_web.dto;

public class PriceAndVolumeDTO {
    private Double price;
    private Double volume;

    public PriceAndVolumeDTO(Double price, Double volume) {
        this.price = price;
        this.volume = volume;
    }

    public Double getPrice() {
        return price;
    }

    public Double getVolume() {
        return volume;
    }
}
