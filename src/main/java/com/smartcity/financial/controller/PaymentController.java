package com.smartcity.financial.controller;

import com.smartcity.financial.dto.PaymentRequest;
import com.smartcity.financial.entity.Transaction;
import com.smartcity.financial.repository.TransactionRepository;
import io.micrometer.core.annotation.Timed;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/payments")
public class PaymentController {

    private final MeterRegistry meterRegistry;
    private final TransactionRepository transactionRepository;

    public PaymentController(MeterRegistry meterRegistry, TransactionRepository transactionRepository) {
        this.meterRegistry = meterRegistry;
        this.transactionRepository = transactionRepository;
    }

    @PostMapping("/process")
    @Timed(value = "smartcity.payment.time", description = "Time taken to process payment")
    public ResponseEntity<Map<String, Object>> processPayment(@RequestBody PaymentRequest request) {
        meterRegistry.counter("smartcity.payments.processed.count").increment();

    
        Transaction transaction = Transaction.builder()
                .userId(request.getUserId())
                .serviceId(request.getServiceId())
                .amount(request.getAmount())
                .status("SUCCESS")
                .build();

        Transaction saved = transactionRepository.save(transaction);

        
        Map<String, Object> response = new HashMap<>();
        response.put("transactionId", saved.getId());
        response.put("status", saved.getStatus());
        response.put("amountProcessed", saved.getAmount());
        response.put("serviceId", saved.getServiceId());
        response.put("createdAt", saved.getTimestamp());
        response.put("message", "Smart City payment completed and persisted successfully.");

        return ResponseEntity.ok(response);
    }
}