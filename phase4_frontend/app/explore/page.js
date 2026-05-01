"use client";

import Header from "../components/Header";
import Link from "next/link";

const categories = [
  {
    slug: "equity",
    title: "Equity Funds",
    icon: "monitoring",
    color: "indigo",
    badge: "+2.4%",
    badgeColor: "emerald",
    description: "Growth-focused large-cap and mid-cap equity funds with strong track records.",
    funds: [
      { name: "HDFC Large Cap Fund", nav: "₹924.15", expense: "1.74%", rating: "★★★★★", minSIP: "₹500" },
      { name: "HDFC Mid-Cap Opportunities Fund", nav: "₹412.80", expense: "1.64%", rating: "★★★★", minSIP: "₹500" },
      { name: "HDFC Small Cap Fund", nav: "₹118.25", expense: "1.82%", rating: "★★★★", minSIP: "₹500" },
      { name: "HDFC Flexi Cap Fund", nav: "₹1,820.50", expense: "1.56%", rating: "★★★★★", minSIP: "₹100" },
    ],
  },
  {
    slug: "debt",
    title: "Debt Funds",
    icon: "account_balance",
    color: "blue",
    badge: "AAA",
    badgeColor: "blue",
    description: "Fixed income funds with focus on capital preservation and steady returns.",
    funds: [
      { name: "HDFC Corporate Bond Fund", nav: "₹28.92", expense: "0.60%", rating: "★★★★★", minSIP: "₹500" },
      { name: "HDFC Short Term Debt Fund", nav: "₹28.15", expense: "0.65%", rating: "★★★★", minSIP: "₹500" },
      { name: "HDFC Overnight Fund", nav: "₹3,245.10", expense: "0.10%", rating: "★★★★★", minSIP: "₹500" },
      { name: "HDFC Gilt Fund", nav: "₹47.80", expense: "0.70%", rating: "★★★", minSIP: "₹500" },
    ],
  },
  {
    slug: "hybrid",
    title: "Hybrid Funds",
    icon: "layers",
    color: "purple",
    badge: "HEDGED",
    badgeColor: "purple",
    description: "Balanced allocation across equity and debt for optimal risk-adjusted returns.",
    funds: [
      { name: "HDFC Balanced Advantage Fund", nav: "₹420.75", expense: "1.48%", rating: "★★★★★", minSIP: "₹500" },
      { name: "HDFC Hybrid Equity Fund", nav: "₹98.40", expense: "1.65%", rating: "★★★★", minSIP: "₹500" },
      { name: "HDFC Multi-Asset Fund", nav: "₹62.30", expense: "1.30%", rating: "★★★★", minSIP: "₹500" },
      { name: "HDFC ELSS Tax Saver Fund", nav: "₹1,102.85", expense: "1.78%", rating: "★★★★★", minSIP: "₹500" },
    ],
  },
];

export default function ExplorePage() {
  return (
    <div className="editorial-gradient min-h-screen relative overflow-hidden">
      <div className="mesh-orb w-[600px] h-[600px] bg-indigo-600/10 top-[-200px] right-[-100px]" style={{ animationDelay: "0s" }}></div>
      <div className="mesh-orb w-[400px] h-[400px] bg-purple-500/8 bottom-[20%] left-[-100px]" style={{ animationDelay: "7s" }}></div>

      <Header />

      <main className="max-w-7xl mx-auto px-6 sm:px-8 relative z-10 pt-16 pb-24">
        <div className="text-center mb-16">
          <span className="text-[10px] text-indigo-400 uppercase tracking-[0.3em] font-semibold">Asset Intelligence</span>
          <h1 className="font-[Newsreader] text-4xl md:text-5xl mt-3 text-white">Explore Fund Categories</h1>
          <p className="text-slate-400 mt-4 max-w-xl mx-auto">Browse HDFC mutual fund schemes by category. Click any fund to get detailed AI-powered analysis.</p>
        </div>

        <div className="space-y-16">
          {categories.map((cat) => (
            <section key={cat.slug} id={cat.slug} className="scroll-mt-24">
              <div className="flex items-center gap-4 mb-6">
                <div className={`w-12 h-12 rounded-xl bg-${cat.color}-500/10 flex items-center justify-center`}>
                  <span className={`material-symbols-outlined text-${cat.color}-400 text-xl`}>{cat.icon}</span>
                </div>
                <div>
                  <h2 className="font-[Newsreader] text-2xl text-white">{cat.title}</h2>
                  <p className="text-sm text-slate-400">{cat.description}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {cat.funds.map((fund) => (
                  <Link
                    key={fund.name}
                    href={`/chat?q=${encodeURIComponent(`Tell me about ${fund.name}`)}`}
                    className="glass-panel-hover p-6 rounded-2xl group cursor-pointer"
                  >
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-sm font-semibold text-white group-hover:text-indigo-200 transition-colors">{fund.name}</h3>
                      <span className="material-symbols-outlined text-slate-600 group-hover:text-indigo-400 transition-colors text-lg">arrow_forward_ios</span>
                    </div>
                    <div className="grid grid-cols-4 gap-3">
                      <div>
                        <div className="text-[10px] text-slate-500 uppercase tracking-wider">NAV</div>
                        <div className="text-sm font-mono text-slate-300 mt-0.5">{fund.nav}</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-500 uppercase tracking-wider">Expense</div>
                        <div className="text-sm font-mono text-slate-300 mt-0.5">{fund.expense}</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-500 uppercase tracking-wider">Rating</div>
                        <div className="text-sm text-amber-400 mt-0.5">{fund.rating}</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-500 uppercase tracking-wider">Min SIP</div>
                        <div className="text-sm font-mono text-slate-300 mt-0.5">{fund.minSIP}</div>
                      </div>
                    </div>
                    <div className="mt-3 pt-3 border-t border-white/5 flex items-center gap-2 text-[10px] text-indigo-400 font-semibold uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity">
                      <span className="material-symbols-outlined text-xs">smart_toy</span>
                      <span>Get AI Analysis</span>
                    </div>
                  </Link>
                ))}
              </div>
            </section>
          ))}
        </div>
      </main>

      {/* FAB */}
      <Link
        href="/chat"
        className="fixed bottom-8 right-8 z-50 bg-gradient-to-r from-indigo-600 to-indigo-500 text-white p-4 rounded-2xl shadow-2xl shadow-indigo-500/30 hover:shadow-indigo-500/50 hover:scale-105 transition-all active:scale-95 group flex items-center gap-2"
      >
        <span className="material-symbols-outlined text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>chat_bubble</span>
        <span className="max-w-0 overflow-hidden group-hover:max-w-[150px] transition-all duration-300 whitespace-nowrap text-sm font-medium">Ask AI</span>
      </Link>
    </div>
  );
}
