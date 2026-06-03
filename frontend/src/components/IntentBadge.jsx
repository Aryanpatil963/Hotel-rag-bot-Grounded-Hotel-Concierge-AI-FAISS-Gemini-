import React from 'react';

export default function IntentBadge({ intent, confidence, variant = 'details' }) {
  if (!intent) return null;

  // Format intent name to readable label
  const formatIntentName = (name) => {
    switch (name) {
      case 'booking_inquiry':
        return 'Booking Inquiry';
      case 'amenity_question':
        return 'Amenity Question';
      case 'complaint':
        return 'Complaint';
      case 'staff_command':
        return 'Staff Command';
      case 'other':
        return 'Other';
      default:
        return name.replace('_', ' ');
    }
  };

  const formattedIntent = formatIntentName(intent);
  const confidencePercent = Math.round(confidence * 100);

  if (variant === 'details') {
    return (
      <div className="inline-flex items-center gap-1.5 px-3 py-1 border border-brand-secondary/30 bg-[#FFFDF6] text-[#B8962D] rounded-full font-body text-[11px] font-semibold tracking-wide">
        <span>Intent: {formattedIntent}</span>
        <span className="text-brand-tertiary/40">|</span>
        <span>Confidence: {confidencePercent}%</span>
      </div>
    );
  }

  // Simple variant (used in admin query table)
  const getBadgeStyles = (type) => {
    switch (type) {
      case 'booking_inquiry':
        return 'bg-brand-primary/10 text-brand-primary border border-brand-primary/20';
      case 'amenity_question':
        return 'bg-brand-secondary/15 text-[#9E801E] border border-brand-secondary/30';
      case 'complaint':
        return 'bg-red-50 text-red-700 border border-red-200';
      case 'staff_command':
        return 'bg-brand-tertiary/10 text-brand-tertiary border border-brand-tertiary/20';
      default:
        return 'bg-gray-100 text-gray-700 border border-gray-200';
    }
  };

  return (
    <span className={`inline-block px-2.5 py-0.5 rounded-full font-body text-[10px] font-bold uppercase tracking-wider ${getBadgeStyles(intent)}`}>
      {intent === 'booking_inquiry' ? 'BOOKING' : 
       intent === 'amenity_question' ? 'AMENITY' : 
       intent === 'staff_command' ? 'STAFF CMD' : 
       intent.replace('_', ' ')}
    </span>
  );
}
