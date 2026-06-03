import React from 'react';

export default function LanguageSwitcher({ language, setLanguage }) {
  const options = [
    { code: 'en', label: 'English' },
    { code: 'hi', label: 'Hindi' },
    { code: 'hinglish', label: 'Hinglish' },
  ];

  return (
    <div className="flex items-center gap-4 text-xs font-body font-medium">
      {options.map((opt) => (
        <button
          key={opt.code}
          onClick={() => setLanguage(opt.code)}
          className={`pb-1 transition-all ${
            language === opt.code
              ? 'text-brand-secondary border-b-2 border-brand-secondary font-bold'
              : 'text-brand-tertiary hover:text-brand-secondary'
          }`}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}
