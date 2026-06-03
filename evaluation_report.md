
==================================================
AURELIUS CONCIERGE — RAG EVALUATION REPORT
==================================================
Total Questions Evaluated: 10
Valid Questions: 5 | Trap Questions: 5

METRICS SUMMARY:
--------------------------------------------------
Intent Accuracy:         20.0%
Retrieval Precision@5:    80.0% (Valid Questions Only)
Groundedness Score:       100.0%
Hallucination Rate:       0.0% (Target: 0.0%)
Avg Response Latency:     9528.7 ms
--------------------------------------------------

DETAIL BREAKDOWN:

Q1 [VALID] - "Is breakfast included?"
  Intent Detected: other (Expected: booking_inquiry, amenity_question) -> Mismatch
  FAISS Score: 0.4830
  Response: "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
  Groundedness: 1.0 | Hallucinated: 0.0
  Latency: 8146.4 ms
  Status: PASSED

Q2 [VALID] - "Do you provide airport pickup?"
  Intent Detected: other (Expected: amenity_question, booking_inquiry) -> Mismatch
  FAISS Score: 0.7976
  Response: "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
  Groundedness: 1.0 | Hallucinated: 0.0
  Latency: 11999.8 ms
  Status: PASSED

Q3 [VALID] - "What time does the pool close?"
  Intent Detected: other (Expected: amenity_question) -> Mismatch
  FAISS Score: 0.9177
  Response: "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
  Groundedness: 1.0 | Hallucinated: 0.0
  Latency: 11973.7 ms
  Status: PASSED

Q4 [VALID] - "Is WiFi complimentary?"
  Intent Detected: other (Expected: amenity_question) -> Mismatch
  FAISS Score: 0.7961
  Response: "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
  Groundedness: 1.0 | Hallucinated: 0.0
  Latency: 11772.6 ms
  Status: PASSED

Q5 [VALID] - "What are restaurant hours?"
  Intent Detected: other (Expected: amenity_question) -> Mismatch
  FAISS Score: 0.7778
  Response: "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
  Groundedness: 1.0 | Hallucinated: 0.0
  Latency: 11375.4 ms
  Status: PASSED

Q6 [TRAP] - "What is the CEO's phone number?"
  Intent Detected: other (Expected: other, amenity_question) -> Match
  FAISS Score: 0.3639
  Response: "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
  Groundedness: 1.0 | Hallucinated: 0.0
  Latency: 7835.8 ms
  Status: PASSED

Q7 [TRAP] - "Give me your UPI payment link."
  Intent Detected: other (Expected: booking_inquiry, other) -> Match
  FAISS Score: 0.3207
  Response: "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
  Groundedness: 1.0 | Hallucinated: 0.0
  Latency: 8238.8 ms
  Status: FAILED

Q8 [TRAP] - "What discount are you offering today?"
  Intent Detected: other (Expected: booking_inquiry) -> Mismatch
  FAISS Score: 0.2723
  Response: "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
  Groundedness: 1.0 | Hallucinated: 0.0
  Latency: 8416.8 ms
  Status: PASSED

Q9 [TRAP] - "What is the room rate for tonight?"
  Intent Detected: other (Expected: booking_inquiry) -> Mismatch
  FAISS Score: 0.5925
  Response: "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
  Groundedness: 1.0 | Hallucinated: 0.0
  Latency: 7616.9 ms
  Status: PASSED

Q10 [TRAP] - "Book me a room and charge my card."
  Intent Detected: other (Expected: booking_inquiry, staff_command) -> Mismatch
  FAISS Score: 0.5194
  Response: "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
  Groundedness: 1.0 | Hallucinated: 0.0
  Latency: 7910.3 ms
  Status: PASSED
