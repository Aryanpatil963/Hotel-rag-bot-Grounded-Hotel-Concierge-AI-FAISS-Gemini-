import React from 'react';
import { FileText, Link, Clock } from 'lucide-react';

export default function SourcePanel({ sources }) {
  // Map files to human-friendly descriptions
  const getSourceMetadata = (filename) => {
    switch (filename.toLowerCase()) {
      case 'amenities.txt':
        return {
          title: 'Amenities Guide',
          desc: 'Official Hotel Amenities',
          type: 'txt'
        };
      case 'hotel_policies.pdf':
        return {
          title: 'Hotel Policies',
          desc: 'Check-in, Pets, Noise Policies',
          type: 'pdf'
        };
      case 'room_info.json':
        return {
          title: 'Room Information',
          desc: 'Suites & Amenities Config',
          type: 'json'
        };
      default:
        return {
          title: filename,
          desc: 'Retrieved context source',
          type: 'doc'
        };
    }
  };

  return (
    <div className="w-[220px] bg-brand-bg border-l border-brand-secondary/20 p-4 flex flex-col justify-between h-screen shrink-0 overflow-y-auto">
      {/* Sources List */}
      <div>
        <h3 className="font-display text-sm font-bold text-brand-primary tracking-wide mb-4">
          Sources Used
        </h3>
        
        {sources && sources.length > 0 ? (
          <div className="space-y-3">
            {sources.map((src, idx) => {
              const meta = getSourceMetadata(src);
              return (
                <div 
                  key={idx} 
                  className="bg-white border border-brand-secondary/15 rounded-lg p-3 shadow-sm hover:shadow-md transition-all duration-300"
                >
                  <div className="flex items-start gap-2.5">
                    <div className="w-8 h-8 rounded bg-brand-primary/5 flex items-center justify-center text-brand-primary shrink-0">
                      <FileText size={16} />
                    </div>
                    <div className="overflow-hidden">
                      <h4 className="font-body text-xs font-bold text-brand-primary truncate">
                        {meta.title}
                      </h4>
                      <p className="font-body text-[10px] text-brand-tertiary mt-0.5 truncate">
                        {meta.desc}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-6 px-4 border border-dashed border-brand-secondary/20 rounded-lg bg-white/50">
            <p className="font-body text-[11px] text-brand-tertiary italic">
              No sources referenced in the current turn.
            </p>
          </div>
        )}
      </div>

      {/* Featured Amenity Card */}
      <div className="mt-8">
        <div className="relative rounded-lg overflow-hidden border border-brand-secondary/30 shadow-lg aspect-[4/5] bg-brand-primary group">
          {/* Image */}
          <img 
            src="/luxury_pool.png" 
            alt="The Sky Pool"
            className="w-full h-full object-cover opacity-75 group-hover:scale-105 transition-transform duration-700"
            onError={(e) => {
              // fallback if public path not yet loaded
              e.target.src = "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?auto=format&fit=crop&q=80&w=600";
            }}
          />
          
          {/* Dark Overlay Gradient */}
          <div className="absolute inset-0 bg-gradient-to-t from-brand-primary via-brand-primary/40 to-transparent" />
          
          {/* Content Overlay */}
          <div className="absolute bottom-0 left-0 right-0 p-4 text-white">
            <span className="font-body text-[9px] uppercase tracking-widest text-brand-secondary font-bold block mb-1">
              Featured Amenity
            </span>
            <h4 className="font-display text-base font-semibold leading-tight mb-2 text-glow">
              The Sky Pool
            </h4>
            <div className="flex items-center gap-1.5 text-[10px] text-gray-200">
              <Clock size={12} className="text-brand-secondary" />
              <span>Open until 10:00 PM tonight</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
