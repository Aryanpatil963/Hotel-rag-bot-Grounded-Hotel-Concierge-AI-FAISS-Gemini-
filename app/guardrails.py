import re

def detect_price_inquiry(query: str, context: str) -> str | None:
    """
    If query mentions room rates, discounts, taxes, booking costs AND price not in retrieved context 
    -> returns standard escalation message.
    """
    price_keywords = [
        r'\bprice(s)?\b', r'\brate(s)?\b', r'\bdiscount(s)?\b', r'\bcost(s)?\b', 
        r'\btax(es)?\b', r'\bcharge(s)?\b', r'\boffer(s)?\b', r'\bcoupon(s)?\b',
        r'\btariff(s)?\b', r'\bfee(s)?\b', r'\bhow much\b', r'\bpayment amount\b'
    ]
    
    query_lower = query.lower()
    matches_price_query = any(re.search(pattern, query_lower) for pattern in price_keywords)
    
    if matches_price_query:
        # Check if context contains price figures or rates (e.g. $, USD, Rs, INR, or digits followed by price keywords)
        # Since our knowledge base has ZERO prices, this is usually False.
        # Let's search context for currency signs or price indicators.
        has_price_in_context = any(char in context for char in ["$", "€", "£", "₹"]) or "USD" in context
        
        if not has_price_in_context:
            return "I couldn't find the room pricing information in the hotel knowledge base. Please contact the hotel front desk."
            
    return None

def detect_payment_inquiry(query: str, context: str) -> str | None:
    """
    If query asks for payment URL, UPI, QR code, card charging AND not in KB
    -> returns standard payment escalation message.
    """
    payment_keywords = [
        r'\bupi\b', r'\bqr\b', r'\blink\b', r'\burl\b', r'\bwebsite\b', 
        r'\bpay(ment)?\b', r'\bcharge my card\b', r'\bcredit card\b', r'\bdebit card\b',
        r'\btransfer\b', r'\bcheckout link\b', r'\bbook me\b'
    ]
    
    query_lower = query.lower()
    matches_payment_query = any(re.search(pattern, query_lower) for pattern in payment_keywords)
    
    if matches_payment_query:
        # Check if context has payment links, UPI IDs, or instructions
        # Since our KB has nothing, this is False.
        has_payment_in_context = "http" in context or "upi@" in context or "pay" in context.lower() and ("network" in context.lower() or "valet" in context.lower()) # check if simple context matches
        # Let's check for explicit URLs or payment handles
        has_explicit_payment = bool(re.search(r'https?://[^\s]+', context)) or "upi" in context.lower() and "link" in context.lower()
        
        if not has_explicit_payment:
            return "I cannot provide payment or booking links unless they exist in the official hotel knowledge base."
            
    return None

def check_context_sufficiency(max_score: float) -> str | None:
    """
    If FAISS retrieval score < 0.60 -> return standard human escalation.
    """
    if max_score < 0.60:
        return "I couldn't find that information in the hotel knowledge base. Let me connect you with a hotel representative."
    return None
