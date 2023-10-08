package com.market_mind.market_mind_web.dto;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;

public class PriceDTO {
    private Double price;
    private LocalDateTime tradeTimestamp;

    public PriceDTO(Double price, LocalDateTime tradeTimestamp) {
        this.price = round(price);
        this.tradeTimestamp = tradeTimestamp;
    }

    // Helper method to round values to two decimal places
    private Double round(Double value) {
        if (value == null) {
            return null;
        }
        BigDecimal bd = new BigDecimal(Double.toString(value));
        bd = bd.setScale(2, RoundingMode.HALF_UP); // Use HALF_UP mode to round towards "nearest neighbor" unless both
                                                   // neighbors are equidistant, in which case round up.
        return bd.doubleValue();
    }

    public Double getPrice() {
        return price;
    }

    public LocalDateTime getTradeTimestamp() {
        return tradeTimestamp;
    }
}
