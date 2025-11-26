import { LucideIcon } from 'lucide-react';
import { ReactNode } from 'react';
import SectionInsightCard from './SectionInsightCard';

interface Insight {
  type: 'danger' | 'warning' | 'good' | 'neutral';
  icon: LucideIcon;
  title: string;
  text: string;
}

interface MetricSectionProps {
  title: string;
  icon: LucideIcon;
  iconColor: string;
  metrics: ReactNode;
  insights?: Insight[];
}

export default function MetricSection({
  title,
  icon: Icon,
  iconColor,
  metrics,
  insights
}: MetricSectionProps) {
  return (
    <div className="bg-slate-800/30 rounded-2xl border border-slate-700/50 overflow-hidden">
      <div className={`px-5 py-3 border-b border-slate-700/50 flex items-center gap-2 ${iconColor}`}>
        <Icon className="w-4 h-4" />
        <h3 className="font-semibold text-sm">{title}</h3>
      </div>
      <div className="p-4">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 mb-4">
          {metrics}
        </div>
        {insights && insights.length > 0 && (
          <div className="space-y-2 pt-3 border-t border-slate-700/30">
            {insights.map((insight, index) => (
              <SectionInsightCard key={index} insight={insight} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
