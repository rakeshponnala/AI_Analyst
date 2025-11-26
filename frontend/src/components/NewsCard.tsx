interface NewsItem {
  title: string;
  source: string;
  url?: string;
}

interface NewsCardProps {
  item: NewsItem;
}

export default function NewsCard({ item }: NewsCardProps) {
  return (
    <a
      href={item.url || '#'}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-3 bg-slate-700/30 hover:bg-slate-700/50 rounded-xl transition-colors group"
    >
      <p className="text-slate-300 text-sm leading-snug group-hover:text-white transition-colors line-clamp-2">
        {item.title}
      </p>
      <p className="text-slate-500 text-xs mt-1">
        {item.source}
      </p>
    </a>
  );
}
