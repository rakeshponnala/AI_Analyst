import { LucideIcon } from 'lucide-react';

interface Insight {
  type: 'danger' | 'warning' | 'good' | 'neutral';
  icon: LucideIcon;
  title: string;
  text: string;
}

interface SectionInsightCardProps {
  insight: Insight;
}

export default function SectionInsightCard({ insight }: SectionInsightCardProps) {
  const bgColors = {
    danger: 'bg-red-500/10 border-red-500/30',
    warning: 'bg-yellow-500/10 border-yellow-500/30',
    good: 'bg-emerald-500/10 border-emerald-500/30',
    neutral: 'bg-slate-500/10 border-slate-500/30'
  };

  const textColors = {
    danger: 'text-red-400',
    warning: 'text-yellow-400',
    good: 'text-emerald-400',
    neutral: 'text-slate-400'
  };

  const Icon = insight.icon;

  return (
    <div className={`p-3 rounded-lg border ${bgColors[insight.type]}`}>
      <div className={`flex items-center gap-2 font-medium text-sm ${textColors[insight.type]}`}>
        <Icon className="w-3.5 h-3.5" />
        <span>{insight.title}</span>
      </div>
      <p className="text-slate-400 text-xs mt-1">{insight.text}</p>
    </div>
  );
}
