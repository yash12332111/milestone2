import Header from "./components/Header";
import Link from "next/link";

export default function Home() {
  const feedItems = [
    { icon: "history_edu", time: "Updated 4m ago", name: "HDFC Large Cap Fund (HDFC-LC)", desc: "Expense ratio verified at 1.74%. NAV tracking Nifty 100 benchmark.", score: 92.4, pct: 92 },
    { icon: "bolt", time: "Critical Insight", name: "HDFC ELSS Tax Saver Fund (HDFC-ELSS)", desc: "Lock-in period: 3 years. Min SIP ₹500. Tax benefit under 80C confirmed.", score: 88.1, pct: 88 },
    { icon: "query_stats", time: "Archived 2h ago", name: "HDFC Mid-Cap Opportunities Fund", desc: "Standard quarter-end audit completed. Exit load 1% within 1 year verified.", score: 99.8, pct: 99, faded: true },
  ];

  const stats = [
    { value: "847", label: "Fund Facts Verified", icon: "verified" },
    { value: "12.4K", label: "Queries Processed", icon: "analytics" },
    { value: "99.7%", label: "Data Accuracy", icon: "shield" },
  ];

  return (
    <div className="editorial-gradient min-h-screen relative overflow-hidden">
      {/* Animated background orbs */}
      <div className="mesh-orb w-[600px] h-[600px] bg-indigo-600/10 top-[-200px] right-[-100px]" style={{ animationDelay: "0s" }}></div>
      <div className="mesh-orb w-[400px] h-[400px] bg-purple-500/8 bottom-[20%] left-[-100px]" style={{ animationDelay: "7s" }}></div>
      <div className="mesh-orb w-[300px] h-[300px] bg-blue-500/5 top-[50%] right-[20%]" style={{ animationDelay: "14s" }}></div>

      <Header />

      <main className="max-w-7xl mx-auto px-6 sm:px-8 relative z-10">
        {/* ═══ HERO ═══ */}
        <section className="pt-24 pb-32 text-center flex flex-col items-center">
          <div className="animate-fade-up">
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/20 mb-8">
              <span className="live-dot"></span>
              <span className="text-primary text-[11px] font-medium tracking-widest uppercase">Live Intelligence Engine</span>
            </span>
          </div>

          <h1 className="animate-fade-up animate-fade-up-d1 font-[Newsreader] text-5xl sm:text-6xl md:text-[72px] leading-[1.05] tracking-tight font-light text-white max-w-5xl mb-8">
            Precision Intelligence for{" "}
            <span className="gradient-text italic font-normal">Smarter Investing.</span>
          </h1>

          <p className="animate-fade-up animate-fade-up-d2 text-lg md:text-xl text-slate-400 max-w-2xl mb-14 leading-relaxed">
            Decipher market complexities with real-time AI fund analysis. Institutional clarity for every high-stakes decision.
          </p>

          {/* Command Center Search */}
          <div className="animate-fade-up animate-fade-up-d3 w-full max-w-3xl">
            <div className="relative group">
              <div className="absolute -inset-[1px] rounded-2xl bg-gradient-to-r from-indigo-500/30 via-purple-500/20 to-indigo-500/30 opacity-0 group-focus-within:opacity-100 transition-opacity duration-500 blur-sm"></div>
              <div className="relative glass-panel rounded-2xl p-2 flex items-center">
                <div className="pl-5 pr-3 text-indigo-400">
                  <span className="material-symbols-outlined text-xl">terminal</span>
                </div>
                <input
                  className="bg-transparent border-none focus:ring-0 w-full text-base text-white placeholder:text-slate-500 py-4 outline-none"
                  placeholder="Search funds, sectors, or enter a prompt for AI analysis..."
                  type="text"
                />
                <div className="hidden sm:flex items-center space-x-1.5 px-4">
                  <kbd className="px-2 py-1 bg-white/5 rounded-md border border-white/10 text-[10px] text-slate-500 font-mono">⌘</kbd>
                  <kbd className="px-2 py-1 bg-white/5 rounded-md border border-white/10 text-[10px] text-slate-500 font-mono">K</kbd>
                </div>
                <Link
                  href="/chat"
                  className="bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white font-semibold text-xs px-8 py-3.5 rounded-xl transition-all mr-1 whitespace-nowrap shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40"
                >
                  ANALYZE →
                </Link>
              </div>
            </div>
          </div>

          {/* Stats Row */}
          <div className="animate-fade-up animate-fade-up-d4 flex flex-wrap justify-center gap-12 mt-16">
            {stats.map((stat, i) => (
              <div key={i} className="flex items-center gap-3 group">
                <span className="material-symbols-outlined text-indigo-400/60 text-lg" style={{ fontVariationSettings: "'FILL' 1" }}>{stat.icon}</span>
                <div className="text-left">
                  <div className="number-highlight text-xl font-semibold font-mono tracking-tight">{stat.value}</div>
                  <div className="text-[10px] text-slate-500 uppercase tracking-widest">{stat.label}</div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ═══ GLOW LINE SEPARATOR ═══ */}
        <div className="glow-line w-full max-w-md mx-auto mb-24 opacity-50"></div>

        {/* ═══ BENTO GRID ═══ */}
        <section className="mb-28">
          <div className="text-center mb-14">
            <span className="text-[10px] text-indigo-400 uppercase tracking-[0.3em] font-semibold">Asset Intelligence</span>
            <h2 className="font-[Newsreader] text-3xl md:text-4xl mt-3 text-white">Explore by Category</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Equity */}
            <Link href="/chat" className="glass-panel-hover p-7 rounded-2xl group cursor-pointer relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative z-10">
                <div className="flex justify-between items-start mb-8">
                  <div className="w-12 h-12 rounded-xl bg-indigo-500/10 flex items-center justify-center group-hover:bg-indigo-500/20 transition-colors">
                    <span className="material-symbols-outlined text-indigo-400 text-xl">monitoring</span>
                  </div>
                  <span className="text-[10px] px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">+2.4%</span>
                </div>
                <h3 className="font-[Newsreader] text-2xl mb-2 text-white group-hover:text-indigo-200 transition-colors">Equity</h3>
                <p className="text-sm text-slate-400 mb-8 leading-relaxed">Growth-focused algorithmic assessment of global large-cap holdings.</p>
                <div className="h-20 w-full relative overflow-hidden rounded-xl bg-gradient-to-r from-indigo-950/50 to-slate-950/30">
                  <svg className="w-full h-full chart-glow" viewBox="0 0 400 80" preserveAspectRatio="none">
                    <defs>
                      <linearGradient id="eq-fill" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="rgba(192,193,255,0.15)" />
                        <stop offset="100%" stopColor="rgba(192,193,255,0)" />
                      </linearGradient>
                    </defs>
                    <path d="M0,60 Q40,55 80,45 T160,35 T240,40 T320,25 T400,15 L400,80 L0,80Z" fill="url(#eq-fill)" />
                    <path d="M0,60 Q40,55 80,45 T160,35 T240,40 T320,25 T400,15" fill="none" stroke="rgba(192,193,255,0.5)" strokeWidth="2" />
                  </svg>
                </div>
              </div>
            </Link>

            {/* Debt */}
            <Link href="/chat" className="glass-panel-hover p-7 rounded-2xl group cursor-pointer relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative z-10">
                <div className="flex justify-between items-start mb-8">
                  <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
                    <span className="material-symbols-outlined text-blue-400 text-xl">account_balance</span>
                  </div>
                  <span className="text-[10px] px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono">AAA</span>
                </div>
                <h3 className="font-[Newsreader] text-2xl mb-2 text-white group-hover:text-blue-200 transition-colors">Debt</h3>
                <p className="text-sm text-slate-400 mb-8 leading-relaxed">Fixed income intelligence and credit risk modeling across jurisdictions.</p>
                <div className="h-20 w-full relative overflow-hidden rounded-xl bg-gradient-to-r from-blue-950/50 to-slate-950/30">
                  <svg className="w-full h-full" viewBox="0 0 400 80" preserveAspectRatio="none">
                    {[30, 90, 150, 210, 270, 330].map((x, i) => (
                      <rect key={i} x={x} y={80 - [45, 35, 55, 40, 50, 60][i]} width="30" height={[45, 35, 55, 40, 50, 60][i]}
                        fill={`rgba(96,165,250,${0.15 + i * 0.04})`} rx="4" />
                    ))}
                  </svg>
                </div>
              </div>
            </Link>

            {/* Hybrid */}
            <Link href="/chat" className="glass-panel-hover p-7 rounded-2xl group cursor-pointer relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative z-10">
                <div className="flex justify-between items-start mb-8">
                  <div className="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center group-hover:bg-purple-500/20 transition-colors">
                    <span className="material-symbols-outlined text-purple-400 text-xl">layers</span>
                  </div>
                  <span className="text-[10px] px-2.5 py-1 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/20 font-mono">HEDGED</span>
                </div>
                <h3 className="font-[Newsreader] text-2xl mb-2 text-white group-hover:text-purple-200 transition-colors">Hybrid</h3>
                <p className="text-sm text-slate-400 mb-8 leading-relaxed">Multi-asset volatility tracking and algorithmic rebalancing strategies.</p>
                <div className="h-20 w-full relative overflow-hidden rounded-xl bg-gradient-to-r from-purple-950/50 to-slate-950/30">
                  <svg className="w-full h-full" viewBox="0 0 400 80" preserveAspectRatio="none">
                    <defs>
                      <linearGradient id="hy-fill" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="rgba(168,85,247,0.12)" />
                        <stop offset="100%" stopColor="transparent" />
                      </linearGradient>
                    </defs>
                    <path d="M0,55 Q60,25 120,40 T240,30 T360,35 L400,40 L400,80 L0,80Z" fill="url(#hy-fill)" />
                    <path d="M0,55 Q60,25 120,40 T240,30 T360,35 L400,40" fill="none" stroke="rgba(168,85,247,0.4)" strokeWidth="2" />
                    <path d="M0,50 Q80,45 160,50 T320,45 L400,48" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
                  </svg>
                </div>
              </div>
            </Link>
          </div>
        </section>

        {/* ═══ EDITORIAL INSIGHT ═══ */}
        <section className="mb-28 relative">
          <div className="glass-panel rounded-2xl p-10 md:p-14 relative overflow-hidden">
            {/* Accent bar */}
            <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-indigo-500 via-purple-500 to-transparent"></div>
            {/* Inner glow */}
            <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-indigo-500/5 blur-[80px] pointer-events-none"></div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center relative z-10">
              <div>
                <div className="flex items-center space-x-2 mb-5">
                  <span className="material-symbols-outlined text-indigo-400 text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>auto_awesome</span>
                  <span className="text-[10px] font-semibold text-indigo-400 uppercase tracking-[0.2em]">AI Editorial Insight</span>
                </div>
                <h2 className="font-[Newsreader] text-3xl md:text-4xl mb-6 text-white leading-tight">The Shift in Emerging Market Sentiment</h2>
                <p className="text-base text-slate-400 leading-relaxed mb-8">
                  Our intelligence engine has detected a non-linear correlation between localized interest rate pivots and institutional capital flows within the APAC sector. Fund transparency metrics are now outperforming raw yield expectations.
                </p>
                <Link href="/chat" className="inline-flex items-center gap-2 text-indigo-400 text-xs font-semibold hover:text-indigo-300 transition-all group/link">
                  <span>READ FULL ANALYSIS</span>
                  <span className="material-symbols-outlined text-sm group-hover/link:translate-x-1 transition-transform">arrow_forward</span>
                </Link>
              </div>

              {/* Capital Flow Card */}
              <div className="bg-slate-900/60 rounded-2xl p-6 border border-white/5 shadow-2xl shadow-indigo-500/5">
                <div className="flex justify-between items-center mb-8">
                  <span className="text-[10px] uppercase tracking-[0.2em] text-slate-500 font-semibold">Capital Flow Index</span>
                  <span className="material-symbols-outlined text-slate-600 text-lg">info</span>
                </div>
                <div className="space-y-6">
                  {[
                    { label: "North America", pct: 75, color: "bg-indigo-400" },
                    { label: "Eurozone", pct: 42, color: "bg-blue-400" },
                    { label: "APAC Sector", pct: 89, color: "bg-indigo-400", glow: true },
                  ].map(item => (
                    <div key={item.label}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-slate-300">{item.label}</span>
                        <span className="text-xs font-mono text-slate-500">{item.pct}%</span>
                      </div>
                      <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                        <div
                          className={`${item.color} h-full rounded-full transition-all duration-1000 ${item.glow ? "shadow-[0_0_12px_rgba(192,193,255,0.5)]" : ""}`}
                          style={{ width: `${item.pct}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ═══ INTELLIGENCE FEED ═══ */}
        <section className="mb-28">
          <div className="flex items-end justify-between mb-10">
            <div>
              <span className="text-[10px] text-indigo-400 uppercase tracking-[0.3em] font-semibold">Verified Data</span>
              <h2 className="font-[Newsreader] text-3xl md:text-4xl mt-2 text-white">Recent Intelligence</h2>
            </div>
            <Link href="/chat" className="hidden md:inline-flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-indigo-400 transition-colors group/all">
              <span>VIEW ALL</span>
              <span className="material-symbols-outlined text-sm group-hover/all:translate-x-1 transition-transform">arrow_forward</span>
            </Link>
          </div>

          <div className="space-y-4">
            {feedItems.map((item, idx) => (
              <Link href="/chat" key={item.name}
                className={`glass-panel-hover p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between group cursor-pointer ${item.faded ? "opacity-60" : ""}`}
              >
                <div className="flex items-start space-x-5 mb-4 md:mb-0">
                  <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 ${item.faded ? "bg-white/5 text-slate-600" : "bg-indigo-500/10 text-indigo-400"}`}>
                    <span className="material-symbols-outlined text-lg">{item.icon}</span>
                  </div>
                  <div>
                    <span className={`text-[10px] uppercase tracking-[0.2em] font-semibold ${item.faded ? "text-slate-600" : "text-indigo-400"}`}>{item.time}</span>
                    <h4 className="text-sm font-semibold text-white mt-0.5">{item.name}</h4>
                    <p className="text-xs text-slate-500 mt-1">{item.desc}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-8 pl-16 md:pl-0">
                  <div className="text-right">
                    <div className="number-highlight text-lg font-mono font-semibold">{item.score}</div>
                    <div className="text-[9px] text-slate-600 uppercase tracking-widest mt-0.5">Trust Score</div>
                    <div className="h-1 w-20 bg-white/5 rounded-full mt-2 overflow-hidden">
                      <div className="bg-indigo-400 h-full rounded-full" style={{ width: `${item.pct}%` }}></div>
                    </div>
                  </div>
                  <span className="material-symbols-outlined text-slate-600 group-hover:text-indigo-400 transition-colors">arrow_forward_ios</span>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </main>

      {/* ═══ FOOTER ═══ */}
      <footer className="border-t border-white/5 bg-slate-950/80 backdrop-blur-xl relative z-10">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 py-16 grid grid-cols-1 md:grid-cols-4 gap-16">
          <div className="col-span-1 md:col-span-2">
            <div className="text-xl font-[Newsreader] font-semibold tracking-tight text-white mb-5">FundFacts AI</div>
            <p className="text-sm text-slate-500 max-w-sm mb-8 leading-relaxed">
              The digital ledger of record for the institutional investment ecosystem. Providing clarity through algorithmic precision.
            </p>
            <div className="flex items-center space-x-2 text-emerald-400">
              <span className="live-dot"></span>
              <span className="text-[10px] uppercase tracking-[0.2em]">All Systems Operational</span>
            </div>
          </div>
          <div>
            <h5 className="text-[10px] font-semibold text-slate-400 mb-5 uppercase tracking-[0.2em]">Platform</h5>
            <ul className="space-y-3 text-sm">
              <li><Link href="/chat" className="text-slate-500 hover:text-indigo-400 transition-colors">Market Intelligence</Link></li>
              <li><Link href="/chat" className="text-slate-500 hover:text-indigo-400 transition-colors">Portfolio Benchmarking</Link></li>
              <li><Link href="/chat" className="text-slate-500 hover:text-indigo-400 transition-colors">Sector Insight Feed</Link></li>
            </ul>
          </div>
          <div>
            <h5 className="text-[10px] font-semibold text-slate-400 mb-5 uppercase tracking-[0.2em]">Legal</h5>
            <ul className="space-y-3 text-sm">
              <li><a className="text-slate-500 hover:text-indigo-400 transition-colors" href="#">Institutional Terms</a></li>
              <li><a className="text-slate-500 hover:text-indigo-400 transition-colors" href="#">Privacy Ledger</a></li>
              <li><a className="text-slate-500 hover:text-indigo-400 transition-colors" href="#">Compliance</a></li>
            </ul>
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-6 sm:px-8 pb-8 pt-6 border-t border-white/5 flex flex-col md:flex-row justify-between items-center text-[10px] text-slate-600 uppercase tracking-[0.2em]">
          <span>© 2024 FundFacts AI. All Intelligence Reserved.</span>
          <span className="mt-2 md:mt-0">Mutual Fund investments are subject to market risks.</span>
        </div>
      </footer>

      {/* ═══ FAB ═══ */}
      <Link
        href="/chat"
        className="fixed bottom-8 right-8 z-50 bg-gradient-to-r from-indigo-600 to-indigo-500 text-white p-4 rounded-2xl shadow-2xl shadow-indigo-500/30 hover:shadow-indigo-500/50 hover:scale-105 transition-all active:scale-95 group flex items-center gap-2 badge-pulse"
      >
        <span className="material-symbols-outlined text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>chat_bubble</span>
        <span className="max-w-0 overflow-hidden group-hover:max-w-[150px] transition-all duration-300 whitespace-nowrap text-sm font-medium">Ask AI</span>
      </Link>
    </div>
  );
}
