import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  icon: LucideIcon;
  label: string;
  value: string | number;
  subValue?: string;
  tooltip?: string;
  colorClass: string;
}

export default function MetricCard({
  icon: Icon,
  label,
  value,
  subValue,
  tooltip,
  colorClass
}: MetricCardProps) {
  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-4 group relative">
      <div className="flex items-center gap-2 text-slate-400 text-sm mb-2">
        <Icon className="w-4 h-4" />
        <span>{label}</span>
      </div>
      <div className={`text-xl font-bold ${colorClass}`}>{value}</div>
      {subValue && <div className="text-xs text-slate-500 mt-1">{subValue}</div>}
      {tooltip && (
        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-slate-900 text-slate-300 text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10 border border-slate-700">
          {tooltip}
        </div>
      )}
    </div>
  );
}
