package com.smartcity.financial.dto;

import lombok.Data;

@Data
public class PaymentRequest {
    private Long userId;
    private Long serviceId;
    private Double amount;
}