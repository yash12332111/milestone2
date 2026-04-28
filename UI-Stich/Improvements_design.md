<!-- Fund Details - Editorial v2 -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Newsreader:opsz,wght@6-72,300;6-72,400;6-72,500;6-72,600&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            display: inline-block;
            line-height: 1;
            text-transform: none;
            letter-spacing: normal;
            word-wrap: normal;
            white-space: nowrap;
            direction: ltr;
        }
        .glass-panel {
            background: rgba(18, 33, 49, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .chart-glow {
            filter: drop-shadow(0 0 8px rgba(192, 193, 255, 0.4));
        }
    </style>
<script id="tailwind-config">
        tailwind.config = {
          darkMode: "class",
          theme: {
            extend: {
              "colors": {
                      "on-primary-fixed": "#07006c",
                      "tertiary-container": "#8691a7",
                      "surface-tint": "#c0c1ff",
                      "background": "#051424",
                      "secondary-container": "#3f465c",
                      "outline": "#908fa0",
                      "on-tertiary": "#263143",
                      "inverse-primary": "#494bd6",
                      "on-error-container": "#ffdad6",
                      "surface-container-highest": "#273647",
                      "on-primary-fixed-variant": "#2f2ebe",
                      "on-error": "#690005",
                      "surface-container": "#122131",
                      "on-background": "#d4e4fa",
                      "secondary-fixed-dim": "#bec6e0",
                      "primary-fixed": "#e1e0ff",
                      "outline-variant": "#464554",
                      "tertiary-fixed-dim": "#bcc7de",
                      "surface-variant": "#273647",
                      "on-secondary-fixed-variant": "#3f465c",
                      "surface-container-lowest": "#010f1f",
                      "on-tertiary-fixed": "#111c2d",
                      "surface": "#051424",
                      "on-primary": "#1000a9",
                      "secondary": "#bec6e0",
                      "inverse-surface": "#d4e4fa",
                      "error-container": "#93000a",
                      "on-tertiary-container": "#1f2a3c",
                      "on-surface-variant": "#c7c4d7",
                      "tertiary": "#bcc7de",
                      "on-secondary-fixed": "#131b2e",
                      "on-surface": "#d4e4fa",
                      "on-tertiary-fixed-variant": "#3c475a",
                      "surface-bright": "#2c3a4c",
                      "on-primary-container": "#0d0096",
                      "inverse-on-surface": "#233143",
                      "on-secondary": "#283044",
                      "error": "#ffb4ab",
                      "primary-container": "#8083ff",
                      "secondary-fixed": "#dae2fd",
                      "on-secondary-container": "#adb4ce",
                      "surface-container-high": "#1c2b3c",
                      "surface-dim": "#051424",
                      "primary-fixed-dim": "#c0c1ff",
                      "primary": "#c0c1ff",
                      "tertiary-fixed": "#d8e3fb",
                      "surface-container-low": "#0d1c2d"
              },
              "borderRadius": {
                      "DEFAULT": "0.125rem",
                      "lg": "0.25rem",
                      "xl": "0.5rem",
                      "full": "0.75rem"
              },
              "spacing": {
                      "md": "24px",
                      "sm": "16px",
                      "gutter": "24px",
                      "lg": "48px",
                      "xs": "8px",
                      "margin": "40px",
                      "unit": "4px",
                      "xl": "80px"
              },
              "fontFamily": {
                      "data-mono": ["Inter"],
                      "label-sm": ["Inter"],
                      "headline-lg": ["Newsreader"],
                      "body-lg": ["Inter"],
                      "headline-md": ["Newsreader"],
                      "headline-display": ["Newsreader"],
                      "body-md": ["Inter"]
              },
              "fontSize": {
                      "data-mono": ["14px", {"lineHeight": "1", "letterSpacing": "0.05em", "fontWeight": "500"}],
                      "label-sm": ["12px", {"lineHeight": "1", "fontWeight": "600"}],
                      "headline-lg": ["32px", {"lineHeight": "1.2", "fontWeight": "400"}],
                      "body-lg": ["18px", {"lineHeight": "1.6", "fontWeight": "400"}],
                      "headline-md": ["24px", {"lineHeight": "1.3", "fontWeight": "500"}],
                      "headline-display": ["48px", {"lineHeight": "1.1", "letterSpacing": "-0.02em", "fontWeight": "300"}],
                      "body-md": ["16px", {"lineHeight": "1.5", "fontWeight": "400"}]
              }
            },
          },
        }
    </script>
</head>
<body class="bg-surface text-on-surface font-body-md overflow-x-hidden">
<!-- TopNavBar -->
<nav class="sticky top-0 w-full z-50 flex items-center justify-between px-12 py-4 bg-slate-950/80 backdrop-blur-xl border-b border-white/10 shadow-none transition-all duration-300 ease-in-out">
<div class="flex items-center gap-8">
<span class="text-xl font-serif font-semibold tracking-tighter text-white">FundFacts AI</span>
<div class="hidden md:flex items-center gap-6">
<a class="font-newsreader text-sm tracking-wide text-indigo-400 border-b-2 border-indigo-500 pb-1" href="#">Market</a>
<a class="font-newsreader text-sm tracking-wide text-slate-400 hover:text-slate-200 transition-colors" href="#">Intelligence</a>
<a class="font-newsreader text-sm tracking-wide text-slate-400 hover:text-slate-200 transition-colors" href="#">Portfolio</a>
</div>
</div>
<div class="flex items-center gap-4">
<div class="relative group">
<span class="material-symbols-outlined text-slate-400 hover:text-indigo-400 cursor-pointer transition-colors" data-icon="notifications">notifications</span>
<span class="absolute top-0 right-0 w-2 h-2 bg-primary rounded-full"></span>
</div>
<span class="material-symbols-outlined text-slate-400 hover:text-indigo-400 cursor-pointer transition-colors" data-icon="account_circle">account_circle</span>
</div>
</nav>
<div class="flex">
<!-- SideNavBar -->
<aside class="h-screen w-72 fixed left-0 top-0 border-r border-white/10 rounded-none bg-slate-950/90 backdrop-blur-2xl shadow-2xl shadow-indigo-500/5 hidden lg:flex flex-col pt-20 pb-8 z-40">
<div class="px-6 mb-8">
<div class="flex items-center gap-3">
<img alt="Institutional User Avatar" class="w-10 h-10 rounded-full border border-indigo-500/30" data-alt="professional portrait of a financial analyst in a dark suit with a clean minimalist background" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDI60v2SyI8T50QtmuN0svkTWVGy5lBfZ50m4uDuk4PUwk2vdWECoUx9jVhEfdgeUPyDVzFyzacC3Y4q_9I6AIer9wM0tB04-IiFrPm_VjtauAkAi3lDGSocxKKqccPHLQNfLKNZlOGZ33EilSMPf0yLkdX9yy3DQ8T9tN7QIb90Kn-tvEbxfUdZGjp8mtplIpIPpNPNix5T6d3BWaeZwuAp1oVs2fZaiwaYY2UIMXOssrUIiMpge8P7CH4p-ZZcsYkiGT4tOyMubA"/>
<div>
<h4 class="font-headline-md text-sm text-white">Ledger History</h4>
<p class="text-xs text-slate-500">Institutional Intelligence</p>
</div>
</div>
</div>
<nav class="flex-1 space-y-1">
<div class="font-newsreader text-sm bg-indigo-500/10 text-indigo-400 border-r-2 border-indigo-500 py-3 px-6 flex items-center gap-3 cursor-pointer">
<span class="material-symbols-outlined" data-icon="add_chart">add_chart</span>
<span>New Analysis</span>
</div>
<div class="font-newsreader text-sm text-slate-500 py-3 px-6 hover:bg-white/5 hover:text-white transition-all flex items-center gap-3 cursor-pointer">
<span class="material-symbols-outlined" data-icon="history">history</span>
<span>Search History</span>
</div>
<div class="font-newsreader text-sm text-slate-500 py-3 px-6 hover:bg-white/5 hover:text-white transition-all flex items-center gap-3 cursor-pointer">
<span class="material-symbols-outlined" data-icon="monitoring">monitoring</span>
<span>Fund Benchmarks</span>
</div>
<div class="font-newsreader text-sm text-slate-500 py-3 px-6 hover:bg-white/5 hover:text-white transition-all flex items-center gap-3 cursor-pointer">
<span class="material-symbols-outlined" data-icon="account_balance">account_balance</span>
<span>Sector Insights</span>
</div>
</nav>
<div class="mt-auto space-y-1 pt-8 border-t border-white/5">
<div class="font-newsreader text-sm text-slate-500 py-3 px-6 hover:bg-white/5 hover:text-white transition-all flex items-center gap-3 cursor-pointer">
<span class="material-symbols-outlined" data-icon="cloud_done">cloud_done</span>
<span>System Status</span>
</div>
<div class="font-newsreader text-sm text-slate-500 py-3 px-6 hover:bg-white/5 hover:text-white transition-all flex items-center gap-3 cursor-pointer">
<span class="material-symbols-outlined" data-icon="settings">settings</span>
<span>Settings</span>
</div>
</div>
</aside>
<!-- Main Content -->
<main class="flex-1 lg:ml-72 min-h-screen px-gutter py-xl">
<div class="max-w-6xl mx-auto">
<!-- Header / Editorial Title -->
<header class="mb-xl">
<div class="flex items-center gap-3 mb-xs">
<span class="bg-primary/10 text-primary text-[10px] font-bold uppercase tracking-[0.2em] px-2 py-0.5 rounded-sm">Institutional Grade</span>
<span class="text-slate-500 text-sm">• Updated 2m ago</span>
</div>
<h1 class="font-headline-display text-on-surface mb-xs">Vanguard Global Tech Equity <span class="text-primary font-headline-lg">(VGTE.IV)</span></h1>
<p class="font-body-lg text-tertiary-container max-w-3xl">Strategic focus on high-growth artificial intelligence infrastructure and semiconductor supply chains across North American and East Asian markets.</p>
</header>
<!-- Key Metrics Grid -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-gutter mb-xl">
<div class="glass-panel p-md">
<p class="text-slate-500 text-xs font-semibold uppercase tracking-widest mb-xs">Current NAV</p>
<div class="flex items-baseline gap-2">
<span class="font-headline-lg text-primary text-4xl">$142.84</span>
<span class="text-success text-sm font-data-mono text-emerald-400">+1.24%</span>
</div>
<div class="mt-md h-1 w-full bg-white/5 rounded-full overflow-hidden">
<div class="h-full bg-primary w-3/4"></div>
</div>
<p class="text-[10px] text-slate-500 mt-2">52-WEEK RANGE: $98.12 — $145.20</p>
</div>
<div class="glass-panel p-md">
<p class="text-slate-500 text-xs font-semibold uppercase tracking-widest mb-xs">YTD Returns</p>
<div class="flex items-baseline gap-2">
<span class="font-headline-lg text-white text-4xl">28.4%</span>
<span class="material-symbols-outlined text-primary text-lg" data-icon="trending_up">trending_up</span>
</div>
<p class="text-tertiary-container text-sm mt-md font-body-md">Outperforming benchmark (S&amp;P 500) by +8.2% in current fiscal cycle.</p>
</div>
<div class="glass-panel p-md">
<p class="text-slate-500 text-xs font-semibold uppercase tracking-widest mb-xs">Expense Ratio</p>
<div class="flex items-baseline gap-2">
<span class="font-headline-lg text-white text-4xl">0.08%</span>
<span class="text-slate-500 text-xs">Institutional Select</span>
</div>
<p class="text-tertiary-container text-sm mt-md font-body-md">Optimized for high-volume mandates with waived management fees until Q4.</p>
</div>
</div>
<!-- Sophisticated Performance Chart Area -->
<section class="glass-panel p-lg mb-xl relative overflow-hidden">
<div class="flex justify-between items-start mb-lg">
<div>
<h2 class="font-headline-md text-white">Performance Trajectory</h2>
<p class="text-slate-500 text-sm">Historical net asset value performance over 24 months</p>
</div>
<div class="flex gap-2 bg-slate-900/50 p-1 rounded-lg">
<button class="px-3 py-1 text-xs font-semibold text-primary bg-indigo-500/10 rounded">1Y</button>
<button class="px-3 py-1 text-xs font-semibold text-slate-500 hover:text-white transition-colors">2Y</button>
<button class="px-3 py-1 text-xs font-semibold text-slate-500 hover:text-white transition-colors">5Y</button>
<button class="px-3 py-1 text-xs font-semibold text-slate-500 hover:text-white transition-colors">MAX</button>
</div>
</div>
<!-- Custom Chart Implementation (Stylized) -->
<div class="h-64 w-full relative">
<svg class="w-full h-full overflow-visible" preserveaspectratio="none" viewbox="0 0 1000 200">
<defs>
<lineargradient id="chartGradient" x1="0" x2="0" y1="0" y2="1">
<stop offset="0%" stop-color="rgba(192, 193, 255, 0.2)"></stop>
<stop offset="100%" stop-color="rgba(192, 193, 255, 0)"></stop>
</lineargradient>
</defs>
<!-- Grid Lines -->
<line stroke="rgba(255,255,255,0.05)" stroke-width="1" x1="0" x2="1000" y1="40" y2="40"></line>
<line stroke="rgba(255,255,255,0.05)" stroke-width="1" x1="0" x2="1000" y1="100" y2="100"></line>
<line stroke="rgba(255,255,255,0.05)" stroke-width="1" x1="0" x2="1000" y1="160" y2="160"></line>
<!-- Area -->
<path d="M0,160 Q100,140 200,120 T400,90 T600,110 T800,60 T1000,40 V200 H0 Z" fill="url(#chartGradient)"></path>
<!-- Main Line -->
<path class="chart-glow" d="M0,160 Q100,140 200,120 T400,90 T600,110 T800,60 T1000,40" fill="none" stroke="#c0c1ff" stroke-width="2.5"></path>
<!-- Highlight Point -->
<circle class="animate-pulse" cx="800" cy="60" fill="#c0c1ff" r="4"></circle>
</svg>
<div class="flex justify-between mt-4 text-[10px] text-slate-500 font-data-mono uppercase tracking-widest">
<span>Q1 2022</span>
<span>Q3 2022</span>
<span>Q1 2023</span>
<span>Q3 2023</span>
<span>Current</span>
</div>
</div>
</section>
<!-- Editorial Block: Institutional Insights -->
<div class="grid grid-cols-1 lg:grid-cols-12 gap-xl mb-xl">
<div class="lg:col-span-7">
<div class="flex items-center gap-2 mb-md">
<span class="material-symbols-outlined text-primary" data-icon="auto_awesome">auto_awesome</span>
<h3 class="font-headline-md text-white">AI Sentiment Analysis</h3>
</div>
<div class="prose prose-invert">
<p class="font-headline-lg text-on-surface leading-snug mb-md italic">
                                "The fund exhibits high capital efficiency with a notable shift toward specialized semiconductor lithography providers. Exposure to AI infra remains the primary alpha driver."
                            </p>
<div class="space-y-4 text-tertiary-container font-body-md">
<p>Our proprietary models suggest a 12% upside over the next fiscal quarter based on current supply chain adjustments and projected institutional inflows. The fund's risk profile remains conservative despite the high-growth sector focus, due to its deep position in 'moat' companies.</p>
<div class="flex gap-4 pt-md">
<div class="flex items-center gap-2 px-4 py-2 bg-surface-container rounded-lg border border-white/5">
<span class="text-primary font-bold">Strong Buy</span>
<span class="text-xs text-slate-500">Signal Strength: 88%</span>
</div>
<div class="flex items-center gap-2 px-4 py-2 bg-surface-container rounded-lg border border-white/5">
<span class="text-white font-bold">Alpha Core</span>
<span class="text-xs text-slate-500">Risk Score: 4.2/10</span>
</div>
</div>
</div>
</div>
</div>
<div class="lg:col-span-5">
<div class="glass-panel p-md h-full">
<h4 class="font-newsreader text-lg text-white mb-md">Top Portfolio Holdings</h4>
<div class="space-y-4">
<div class="flex justify-between items-center pb-2 border-b border-white/5">
<div>
<p class="text-white font-semibold">NVIDIA Corporation</p>
<p class="text-xs text-slate-500">NVDA / Semiconductors</p>
</div>
<span class="font-data-mono text-primary">12.4%</span>
</div>
<div class="flex justify-between items-center pb-2 border-b border-white/5">
<div>
<p class="text-white font-semibold">ASML Holding N.V.</p>
<p class="text-xs text-slate-500">ASML / Capital Goods</p>
</div>
<span class="font-data-mono text-primary">8.2%</span>
</div>
<div class="flex justify-between items-center pb-2 border-b border-white/5">
<div>
<p class="text-white font-semibold">Taiwan Semi Manufacturing</p>
<p class="text-xs text-slate-500">TSM / Tech Foundry</p>
</div>
<span class="font-data-mono text-primary">7.9%</span>
</div>
<div class="flex justify-between items-center pb-2 border-b border-white/5">
<div>
<p class="text-white font-semibold">Microsoft Corp</p>
<p class="text-xs text-slate-500">MSFT / Cloud Services</p>
</div>
<span class="font-data-mono text-primary">6.5%</span>
</div>
<button class="w-full text-center py-2 text-xs text-slate-500 hover:text-primary transition-colors font-semibold uppercase tracking-widest">
                                    View Full Ledger (42 Assets)
                                </button>
</div>
</div>
</div>
</div>
<!-- Contextual Footer Metadata -->
<footer class="border-t border-white/10 pt-lg pb-xl flex flex-col md:flex-row justify-between items-start gap-8">
<div class="max-w-xs">
<h5 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">Fund Management</h5>
<p class="text-sm text-slate-500 leading-relaxed">Led by Sarah Jenkins, PhD (Quantitative Analysis) and Michael Chen (Global Equities). Managed from London and Singapore offices.</p>
</div>
<div class="flex gap-gutter">
<button class="bg-primary text-on-primary-fixed px-6 py-3 font-semibold rounded-lg hover:shadow-lg hover:shadow-primary/20 transition-all">Download Prospectus</button>
<button class="border border-white/20 text-white px-6 py-3 font-semibold rounded-lg hover:bg-white/5 transition-all">Request Quote</button>
</div>
</footer>
</div>
</main>
</div>
<!-- Floating AI Prompt (Contextual FAB) -->
<button class="fixed bottom-8 right-8 bg-indigo-600 text-white p-4 rounded-full shadow-2xl hover:scale-110 transition-transform active:scale-95 group flex items-center gap-2">
<span class="material-symbols-outlined" data-icon="chat_bubble" style="font-variation-settings: 'FILL' 1;">chat_bubble</span>
<span class="max-w-0 overflow-hidden group-hover:max-w-xs transition-all duration-300 whitespace-nowrap pr-2">Ask FundFacts AI</span>
</button>
</body></html>

<!-- Landing Page - Editorial v2 -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
          darkMode: "class",
          theme: {
            extend: {
              "colors": {
                      "on-primary-fixed": "#07006c",
                      "tertiary-container": "#8691a7",
                      "surface-tint": "#c0c1ff",
                      "background": "#051424",
                      "secondary-container": "#3f465c",
                      "outline": "#908fa0",
                      "on-tertiary": "#263143",
                      "inverse-primary": "#494bd6",
                      "on-error-container": "#ffdad6",
                      "surface-container-highest": "#273647",
                      "on-primary-fixed-variant": "#2f2ebe",
                      "on-error": "#690005",
                      "surface-container": "#122131",
                      "on-background": "#d4e4fa",
                      "secondary-fixed-dim": "#bec6e0",
                      "primary-fixed": "#e1e0ff",
                      "outline-variant": "#464554",
                      "tertiary-fixed-dim": "#bcc7de",
                      "surface-variant": "#273647",
                      "on-secondary-fixed-variant": "#3f465c",
                      "surface-container-lowest": "#010f1f",
                      "on-tertiary-fixed": "#111c2d",
                      "surface": "#051424",
                      "on-primary": "#1000a9",
                      "secondary": "#bec6e0",
                      "inverse-surface": "#d4e4fa",
                      "error-container": "#93000a",
                      "on-tertiary-container": "#1f2a3c",
                      "on-surface-variant": "#c7c4d7",
                      "tertiary": "#bcc7de",
                      "on-secondary-fixed": "#131b2e",
                      "on-surface": "#d4e4fa",
                      "on-tertiary-fixed-variant": "#3c475a",
                      "surface-bright": "#2c3a4c",
                      "on-primary-container": "#0d0096",
                      "inverse-on-surface": "#233143",
                      "on-secondary": "#283044",
                      "error": "#ffb4ab",
                      "primary-container": "#8083ff",
                      "secondary-fixed": "#dae2fd",
                      "on-secondary-container": "#adb4ce",
                      "surface-container-high": "#1c2b3c",
                      "surface-dim": "#051424",
                      "primary-fixed-dim": "#c0c1ff",
                      "primary": "#c0c1ff",
                      "tertiary-fixed": "#d8e3fb",
                      "surface-container-low": "#0d1c2d"
              },
              "borderRadius": {
                      "DEFAULT": "0.125rem",
                      "lg": "0.25rem",
                      "xl": "0.5rem",
                      "full": "0.75rem"
              },
              "spacing": {
                      "md": "24px",
                      "sm": "16px",
                      "gutter": "24px",
                      "lg": "48px",
                      "xs": "8px",
                      "margin": "40px",
                      "unit": "4px",
                      "xl": "80px"
              },
              "fontFamily": {
                      "data-mono": ["Inter"],
                      "label-sm": ["Inter"],
                      "headline-lg": ["Newsreader"],
                      "body-lg": ["Inter"],
                      "headline-md": ["Newsreader"],
                      "headline-display": ["Newsreader"],
                      "body-md": ["Inter"]
              },
              "fontSize": {
                      "data-mono": ["14px", {"lineHeight": "1", "letterSpacing": "0.05em", "fontWeight": "500"}],
                      "label-sm": ["12px", {"lineHeight": "1", "fontWeight": "600"}],
                      "headline-lg": ["32px", {"lineHeight": "1.2", "fontWeight": "400"}],
                      "body-lg": ["18px", {"lineHeight": "1.6", "fontWeight": "400"}],
                      "headline-md": ["24px", {"lineHeight": "1.3", "fontWeight": "500"}],
                      "headline-display": ["48px", {"lineHeight": "1.1", "letterSpacing": "-0.02em", "fontWeight": "300"}],
                      "body-md": ["16px", {"lineHeight": "1.5", "fontWeight": "400"}]
              }
            },
          },
        }
    </script>
<style>
        .glass-panel {
            background: rgba(18, 33, 49, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .editorial-gradient {
            background: radial-gradient(circle at top right, rgba(73, 75, 214, 0.15), transparent 40%),
                        radial-gradient(circle at bottom left, rgba(192, 193, 255, 0.05), transparent 40%);
        }
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 24;
        }
    </style>
</head>
<body class="bg-surface-dim text-on-surface editorial-gradient min-h-screen">
<!-- TopNavBar -->
<header class="sticky top-0 w-full z-50 flex items-center justify-between px-12 py-4 bg-slate-950/80 backdrop-blur-xl border-b border-white/10">
<div class="text-xl font-serif font-semibold tracking-tighter text-white">FundFacts AI</div>
<nav class="hidden md:flex items-center space-x-8">
<a class="font-newsreader text-sm tracking-wide text-indigo-400 border-b-2 border-indigo-500 pb-1" href="#">Market</a>
<a class="font-newsreader text-sm tracking-wide text-slate-400 hover:text-slate-200 transition-colors" href="#">Intelligence</a>
<a class="font-newsreader text-sm tracking-wide text-slate-400 hover:text-slate-200 transition-colors" href="#">Portfolio</a>
</nav>
<div class="flex items-center space-x-6">
<button class="text-slate-400 hover:text-white transition-all"><span class="material-symbols-outlined" data-icon="notifications">notifications</span></button>
<button class="text-slate-400 hover:text-white transition-all"><span class="material-symbols-outlined" data-icon="account_circle">account_circle</span></button>
</div>
</header>
<main class="max-w-7xl mx-auto px-gutter py-xl">
<!-- Hero Section -->
<section class="mb-xl text-center md:text-left flex flex-col items-center md:items-start">
<span class="text-primary font-label-sm tracking-widest uppercase mb-sm">Institutional Grade Analysis</span>
<h1 class="font-headline-display text-headline-display text-on-surface max-w-4xl mb-md">
                Precision Intelligence for <span class="italic text-primary-container">Smarter Investing.</span>
</h1>
<p class="font-body-lg text-body-lg text-outline-variant max-w-2xl mb-lg">
                Decipher market complexities with real-time AI fund analysis. Our ledger of record provides institutional clarity for every high-stakes decision.
            </p>
<!-- Command Center Search -->
<div class="w-full max-w-3xl glass-panel rounded-xl p-xs flex items-center group focus-within:ring-2 focus-within:ring-primary/30 transition-all">
<div class="px-md text-primary">
<span class="material-symbols-outlined" data-icon="terminal">terminal</span>
</div>
<input class="bg-transparent border-none focus:ring-0 w-full text-body-md font-body-md text-on-surface placeholder:text-outline/50 py-sm" placeholder="Search funds, sectors, or enter a prompt for AI analysis..." type="text"/>
<div class="hidden sm:flex items-center space-x-2 px-md">
<kbd class="px-2 py-1 bg-surface-container-highest rounded border border-outline/20 text-xs text-outline font-data-mono">CMD</kbd>
<kbd class="px-2 py-1 bg-surface-container-highest rounded border border-outline/20 text-xs text-outline font-data-mono">K</kbd>
</div>
<button class="bg-primary hover:bg-primary-container text-on-primary font-label-sm px-lg py-sm rounded-lg transition-all mr-xs">
                    ANALYZE
                </button>
</div>
</section>
<!-- Categories Bento Grid -->
<section class="mb-xl">
<div class="grid grid-cols-1 md:grid-cols-3 gap-gutter">
<!-- Equity Card -->
<div class="glass-panel p-md rounded-xl hover:border-primary/40 transition-all group">
<div class="flex justify-between items-start mb-lg">
<span class="material-symbols-outlined text-primary text-3xl" data-icon="monitoring">monitoring</span>
<span class="text-error font-data-mono text-data-mono">+2.4% VOL</span>
</div>
<h3 class="font-headline-md text-headline-md mb-xs">Equity</h3>
<p class="font-body-md text-body-md text-outline-variant mb-lg">Growth-focused algorithmic assessment of global large-cap holdings.</p>
<div class="h-24 w-full relative overflow-hidden">
<img class="absolute inset-0 w-full h-full object-cover opacity-40 group-hover:opacity-60 transition-opacity" data-alt="minimal abstract indigo line chart against a dark background representing equity growth trends" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC49jwBI4PYfzWbqY8olPdFQTtfX10cjeoXwoLPaj3wexXG77I7Asr_ZdPfrbSVDsbzz4obHqIeWbX32wbfpjea2pEJTqdEavogVxHWjhIzqKP9g2S-xTiZYy6dgSAwT8GyV68k7wXi6JyG4F6BxXqJmCZZnqtmOXVZsXA4Oe60vtszn9ACYZw8kDWoz4Tlam6aj1OsgHQXd2jwsTSZh3MQLsn6nJbSOPkKHi1QNeAUCe1WlLYPnCc7Kv_0rCPxekBTQtdjkC3A-zg"/>
</div>
</div>
<!-- Debt Card -->
<div class="glass-panel p-md rounded-xl hover:border-primary/40 transition-all group">
<div class="flex justify-between items-start mb-lg">
<span class="material-symbols-outlined text-primary text-3xl" data-icon="account_balance">account_balance</span>
<span class="text-primary-fixed font-data-mono text-data-mono">AAA RATED</span>
</div>
<h3 class="font-headline-md text-headline-md mb-xs">Debt</h3>
<p class="font-body-md text-body-md text-outline-variant mb-lg">Fixed income intelligence and credit risk modeling across 40 jurisdictions.</p>
<div class="h-24 w-full relative overflow-hidden">
<img class="absolute inset-0 w-full h-full object-cover opacity-40 group-hover:opacity-60 transition-opacity" data-alt="minimal technical bars and data points in indigo representing fixed income distributions" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCnXeZeawb0sFB5jWXcLPN0NJk8pPGhEDCt0EmDIGpxBKjiuDuWJ1n2fTXA-ndt5vorAHmLYQ2OFydeU5D9Ee3kLkRme8LfFjSfYlXGS70HwunVw3n9XjGo-NeV3Shtt-n06WrNgTl0XqOASaFXYGZPmF78ULqAVSd4i6LMHVPkuF1FkSfnAaj2fUwTE6G04mZDZcFT6sVZyROVhrHWl5nj5_gqA5LeVIrzUkEiD5ULiANTerB9ImleIkdFXCpSPpyFHbsk5Yq8buE"/>
</div>
</div>
<!-- Hybrid Card -->
<div class="glass-panel p-md rounded-xl hover:border-primary/40 transition-all group">
<div class="flex justify-between items-start mb-lg">
<span class="material-symbols-outlined text-primary text-3xl" data-icon="layers">layers</span>
<span class="text-tertiary-container font-data-mono text-data-mono">HEDGED</span>
</div>
<h3 class="font-headline-md text-headline-md mb-xs">Hybrid</h3>
<p class="font-body-md text-body-md text-outline-variant mb-lg">Multi-asset volatility tracking and algorithmic rebalancing strategies.</p>
<div class="h-24 w-full relative overflow-hidden">
<img class="absolute inset-0 w-full h-full object-cover opacity-40 group-hover:opacity-60 transition-opacity" data-alt="abstract geometric layers in deep indigo and slate representing multi-asset portfolios" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC23zGokk3Pz7RzrwPsAVoZJ-TFOXWRJAxaRoAcHY8OkCrVTXsr5WWnwFEYFLXS7xB4xiywVLF9GF-zoyk5T97Ov7XjZVnKxswiHlR66FZx-rDBzyB73s376OVwLDyIl8LCd5xnLcXYFD1UCjgeYd5kreAZNCleEIPngHfz_VAvs_JVf5T8evv8hoa6ljCnq01ReC097xORycb7TUDaIPapof9EyGZ7PgbXieuLkO_SAilrPIw5CAmkR7hofOVy_gIV1F8w1id1dBc"/>
</div>
</div>
</div>
</section>
<!-- Editorial Block: AI Insight -->
<section class="mb-xl glass-panel p-lg rounded-none relative overflow-hidden">
<div class="absolute top-0 left-0 w-1 h-full bg-primary"></div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-xl items-center">
<div>
<div class="flex items-center space-x-2 mb-sm">
<span class="material-symbols-outlined text-primary" data-icon="auto_awesome">auto_awesome</span>
<span class="font-label-sm text-primary uppercase tracking-tighter">AI Editorial Insight</span>
</div>
<h2 class="font-headline-lg text-headline-lg mb-md">The Shift in Emerging Market Sentiment</h2>
<p class="font-body-md text-body-md text-on-surface-variant leading-relaxed mb-lg">
                        Our intelligence engine has detected a non-linear correlation between localized interest rate pivots and institutional capital flows within the APAC sector. Unlike previous cycles, the "Flight to Quality" is being superseded by a "Flight to Clarity," where fund transparency metrics are now outperforming raw yield expectations. 
                    </p>
<button class="text-primary font-label-sm border-b border-primary pb-1 hover:text-primary-container hover:border-primary-container transition-all">
                        READ FULL ANALYSIS
                    </button>
</div>
<div class="bg-surface-container rounded-xl p-md border border-white/5 shadow-2xl shadow-indigo-500/10">
<div class="flex justify-between items-center mb-md">
<span class="font-data-mono text-data-mono text-outline">CAPITAL FLOW INDEX</span>
<span class="material-symbols-outlined text-outline" data-icon="info">info</span>
</div>
<div class="space-y-4">
<div class="flex items-center justify-between">
<span class="text-sm font-label-sm">North America</span>
<div class="w-1/2 h-1 bg-surface-variant rounded-full overflow-hidden">
<div class="bg-primary h-full w-[75%]"></div>
</div>
</div>
<div class="flex items-center justify-between">
<span class="text-sm font-label-sm">Eurozone</span>
<div class="w-1/2 h-1 bg-surface-variant rounded-full overflow-hidden">
<div class="bg-primary h-full w-[42%]"></div>
</div>
</div>
<div class="flex items-center justify-between">
<span class="text-sm font-label-sm">APAC Sector</span>
<div class="w-1/2 h-1 bg-surface-variant rounded-full overflow-hidden">
<div class="bg-primary h-full w-[89%] shadow-[0_0_10px_rgba(192,193,255,0.5)]"></div>
</div>
</div>
</div>
</div>
</div>
</section>
<!-- Recent Intelligence Feed -->
<section>
<div class="flex items-end justify-between mb-lg">
<div>
<h2 class="font-headline-lg text-headline-lg">Recent Intelligence</h2>
<p class="font-body-md text-outline-variant">Verified fund facts and automated ledger updates.</p>
</div>
<button class="hidden md:block font-label-sm text-outline hover:text-white transition-colors">VIEW ALL HISTORY</button>
</div>
<div class="space-y-gutter">
<!-- Feed Item 1 -->
<div class="glass-panel p-md flex flex-col md:flex-row md:items-center justify-between group hover:bg-white/5 transition-all">
<div class="flex items-start space-x-md mb-sm md:mb-0">
<div class="w-12 h-12 rounded flex items-center justify-center bg-primary/10 text-primary shrink-0">
<span class="material-symbols-outlined" data-icon="history_edu">history_edu</span>
</div>
<div>
<span class="font-data-mono text-xs text-primary uppercase">Updated 4m ago</span>
<h4 class="font-headline-md text-body-md font-semibold">Vanguard Total Bond Market (VBTLX)</h4>
<p class="text-sm text-outline-variant">Rebalancing detected in sovereign debt allocations. Exposure shift: +1.2%.</p>
</div>
</div>
<div class="flex items-center space-x-lg pl-12 md:pl-0">
<div class="text-right">
<div class="font-data-mono text-on-surface">92.4 <span class="text-[10px] text-outline">TRUST SCORE</span></div>
<div class="h-1 w-20 bg-surface-variant rounded-full mt-1">
<div class="bg-primary h-full w-[92%]"></div>
</div>
</div>
<span class="material-symbols-outlined text-outline group-hover:text-primary transition-colors" data-icon="arrow_forward_ios">arrow_forward_ios</span>
</div>
</div>
<!-- Feed Item 2 -->
<div class="glass-panel p-md flex flex-col md:flex-row md:items-center justify-between group hover:bg-white/5 transition-all">
<div class="flex items-start space-x-md mb-sm md:mb-0">
<div class="w-12 h-12 rounded flex items-center justify-center bg-primary/10 text-primary shrink-0">
<span class="material-symbols-outlined" data-icon="bolt">bolt</span>
</div>
<div>
<span class="font-data-mono text-xs text-primary uppercase">Critical Insight</span>
<h4 class="font-headline-md text-body-md font-semibold">BlackRock iShares Core S&amp;P 500 (IVV)</h4>
<p class="text-sm text-outline-variant">Abnormal buy-side pressure detected in consumer discretionary sector within fund.</p>
</div>
</div>
<div class="flex items-center space-x-lg pl-12 md:pl-0">
<div class="text-right">
<div class="font-data-mono text-on-surface">88.1 <span class="text-[10px] text-outline">TRUST SCORE</span></div>
<div class="h-1 w-20 bg-surface-variant rounded-full mt-1">
<div class="bg-primary h-full w-[88%]"></div>
</div>
</div>
<span class="material-symbols-outlined text-outline group-hover:text-primary transition-colors" data-icon="arrow_forward_ios">arrow_forward_ios</span>
</div>
</div>
<!-- Feed Item 3 -->
<div class="glass-panel p-md flex flex-col md:flex-row md:items-center justify-between group hover:bg-white/5 transition-all opacity-70">
<div class="flex items-start space-x-md mb-sm md:mb-0">
<div class="w-12 h-12 rounded flex items-center justify-center bg-white/5 text-outline shrink-0">
<span class="material-symbols-outlined" data-icon="query_stats">query_stats</span>
</div>
<div>
<span class="font-data-mono text-xs text-outline uppercase">Archived 2h ago</span>
<h4 class="font-headline-md text-body-md font-semibold">Fidelity Contrafund (FCNTX)</h4>
<p class="text-sm text-outline-variant">Standard quarter-end audit completed. Metadata verification successful.</p>
</div>
</div>
<div class="flex items-center space-x-lg pl-12 md:pl-0">
<div class="text-right">
<div class="font-data-mono text-on-surface">99.8 <span class="text-[10px] text-outline">TRUST SCORE</span></div>
<div class="h-1 w-20 bg-surface-variant rounded-full mt-1">
<div class="bg-primary h-full w-[99%]"></div>
</div>
</div>
<span class="material-symbols-outlined text-outline group-hover:text-primary transition-colors" data-icon="arrow_forward_ios">arrow_forward_ios</span>
</div>
</div>
</div>
</section>
</main>
<!-- Footer -->
<footer class="mt-xl border-t border-white/10 bg-slate-950 py-lg">
<div class="max-w-7xl mx-auto px-gutter grid grid-cols-1 md:grid-cols-4 gap-xl">
<div class="col-span-1 md:col-span-2">
<div class="text-xl font-serif font-semibold tracking-tighter text-white mb-md">FundFacts AI</div>
<p class="font-body-md text-outline-variant max-w-sm mb-lg">
                    The digital ledger of record for the institutional investment ecosystem. Providing clarity through algorithmic precision.
                </p>
<div class="flex items-center space-x-md">
<div class="flex items-center space-x-1 text-primary">
<span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">cloud_done</span>
<span class="text-[10px] font-data-mono uppercase tracking-widest">System Status: Optimal</span>
</div>
</div>
</div>
<div>
<h5 class="font-label-sm text-on-surface mb-md">PLATFORM</h5>
<ul class="space-y-sm text-sm text-outline">
<li><a class="hover:text-primary transition-colors" href="#">Market Intelligence</a></li>
<li><a class="hover:text-primary transition-colors" href="#">Portfolio Benchmarking</a></li>
<li><a class="hover:text-primary transition-colors" href="#">Sector Insight Feed</a></li>
</ul>
</div>
<div>
<h5 class="font-label-sm text-on-surface mb-md">LEGAL</h5>
<ul class="space-y-sm text-sm text-outline">
<li><a class="hover:text-primary transition-colors" href="#">Institutional Terms</a></li>
<li><a class="hover:text-primary transition-colors" href="#">Privacy Ledger</a></li>
<li><a class="hover:text-primary transition-colors" href="#">Compliance</a></li>
</ul>
</div>
</div>
<div class="max-w-7xl mx-auto px-gutter mt-xl pt-md border-t border-white/5 flex flex-col md:flex-row justify-between items-center text-[10px] font-data-mono text-outline/50 uppercase tracking-[0.2em]">
<span>© 2024 FUNDFACTS AI. ALL INTELLIGENCE RESERVED.</span>
<span class="mt-xs md:mt-0">LAST SYNC: OCT 24, 2024 14:32:01 UTC</span>
</div>
</footer>
</body></html>

<!-- Chat Interface - Editorial v2 -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>FundFacts AI | Institutional Intelligence</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Newsreader:ital,wght@0,300;0,400;0,500;0,600;1,400&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "on-primary-fixed": "#07006c",
                        "tertiary-container": "#8691a7",
                        "surface-tint": "#c0c1ff",
                        "background": "#051424",
                        "secondary-container": "#3f465c",
                        "outline": "#908fa0",
                        "on-tertiary": "#263143",
                        "inverse-primary": "#494bd6",
                        "on-error-container": "#ffdad6",
                        "surface-container-highest": "#273647",
                        "on-primary-fixed-variant": "#2f2ebe",
                        "on-error": "#690005",
                        "surface-container": "#122131",
                        "on-background": "#d4e4fa",
                        "secondary-fixed-dim": "#bec6e0",
                        "primary-fixed": "#e1e0ff",
                        "outline-variant": "#464554",
                        "tertiary-fixed-dim": "#bcc7de",
                        "surface-variant": "#273647",
                        "on-secondary-fixed-variant": "#3f465c",
                        "surface-container-lowest": "#010f1f",
                        "on-tertiary-fixed": "#111c2d",
                        "surface": "#051424",
                        "on-primary": "#1000a9",
                        "secondary": "#bec6e0",
                        "inverse-surface": "#d4e4fa",
                        "error-container": "#93000a",
                        "on-tertiary-container": "#1f2a3c",
                        "on-surface-variant": "#c7c4d7",
                        "tertiary": "#bcc7de",
                        "on-secondary-fixed": "#131b2e",
                        "on-surface": "#d4e4fa",
                        "on-tertiary-fixed-variant": "#3c475a",
                        "surface-bright": "#2c3a4c",
                        "on-primary-container": "#0d0096",
                        "inverse-on-surface": "#233143",
                        "on-secondary": "#283044",
                        "error": "#ffb4ab",
                        "primary-container": "#8083ff",
                        "secondary-fixed": "#dae2fd",
                        "on-secondary-container": "#adb4ce",
                        "surface-container-high": "#1c2b3c",
                        "surface-dim": "#051424",
                        "primary-fixed-dim": "#c0c1ff",
                        "primary": "#c0c1ff",
                        "tertiary-fixed": "#d8e3fb",
                        "surface-container-low": "#0d1c2d"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "spacing": {
                        "md": "24px",
                        "sm": "16px",
                        "gutter": "24px",
                        "lg": "48px",
                        "xs": "8px",
                        "margin": "40px",
                        "unit": "4px",
                        "xl": "80px"
                    },
                    "fontFamily": {
                        "data-mono": ["Inter"],
                        "label-sm": ["Inter"],
                        "headline-lg": ["Newsreader"],
                        "body-lg": ["Inter"],
                        "headline-md": ["Newsreader"],
                        "headline-display": ["Newsreader"],
                        "body-md": ["Inter"]
                    },
                    "fontSize": {
                        "data-mono": ["14px", {"lineHeight": "1", "letterSpacing": "0.05em", "fontWeight": "500"}],
                        "label-sm": ["12px", {"lineHeight": "1", "fontWeight": "600"}],
                        "headline-lg": ["32px", {"lineHeight": "1.2", "fontWeight": "400"}],
                        "body-lg": ["18px", {"lineHeight": "1.6", "fontWeight": "400"}],
                        "headline-md": ["24px", {"lineHeight": "1.3", "fontWeight": "500"}],
                        "headline-display": ["48px", {"lineHeight": "1.1", "letterSpacing": "-0.02em", "fontWeight": "300"}],
                        "body-md": ["16px", {"lineHeight": "1.5", "fontWeight": "400"}]
                    }
                },
            },
        }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .glass-panel {
            background: rgba(18, 33, 49, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .editorial-border {
            border-left: 1px solid rgba(192, 193, 255, 0.3);
        }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #464554; border-radius: 10px; }
    </style>
</head>
<body class="bg-background text-on-surface font-body-md selection:bg-primary/30">
<!-- TopNavBar -->
<nav class="sticky top-0 w-full z-50 flex items-center justify-between px-12 py-4 bg-slate-950/80 backdrop-blur-xl border-b border-white/10 shadow-none">
<div class="flex items-center gap-8">
<span class="text-xl font-serif font-semibold tracking-tighter text-white">FundFacts AI</span>
<div class="hidden md:flex gap-6 items-center">
<a class="font-newsreader text-sm tracking-wide text-indigo-400 border-b-2 border-indigo-500 pb-1 transition-all duration-300 ease-in-out" href="#">Intelligence</a>
<a class="font-newsreader text-sm tracking-wide text-slate-400 hover:text-slate-200 transition-colors transition-all duration-300 ease-in-out" href="#">Market</a>
<a class="font-newsreader text-sm tracking-wide text-slate-400 hover:text-slate-200 transition-colors transition-all duration-300 ease-in-out" href="#">Portfolio</a>
</div>
</div>
<div class="flex items-center gap-4">
<div class="relative group">
<span class="material-symbols-outlined text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 text-sm">search</span>
<input class="bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-1.5 text-xs focus:ring-1 focus:ring-indigo-500 outline-none w-64 transition-all" placeholder="Global Identifier Search..." type="text"/>
</div>
<button class="text-slate-400 hover:text-white transition-colors"><span class="material-symbols-outlined">notifications</span></button>
<button class="text-slate-400 hover:text-white transition-colors"><span class="material-symbols-outlined">account_circle</span></button>
</div>
</nav>
<div class="flex h-[calc(100vh-64px)] overflow-hidden">
<!-- SideNavBar (Left Sidebar) -->
<aside class="h-screen w-72 fixed left-0 top-0 border-r rounded-none bg-slate-950/90 backdrop-blur-2xl border-white/10 shadow-2xl shadow-indigo-500/5 flex flex-col h-full pt-20 pb-8 z-40">
<div class="px-6 mb-6">
<div class="flex items-center gap-3 p-3 glass-panel rounded-xl mb-8">
<img alt="Institutional User" class="w-10 h-10 rounded-full object-cover grayscale" data-alt="close-up portrait of professional executive in soft lighting dark studio background" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBSHkY-rVA97J981kboOwtezZk051JaO3VKjuxSpuq5w4vdw3P7whceyroG-sxnjoBkitzu7nHcgxw74mK3ujLwUSpoaZFtA0Un7WCR1sBmB4Mdug65eac3uNjMnsQeb3D9Kocp1qSj-h3IN5FFfT45Mm7MAbYF9v3iPwS28CvlCZmQvM3hD1tUk9CdTnIMNHTbqTPMDbco8U7I00OHYTaX9jChfhloaxjvuseVE0l8wp6C8WfTMjCBE3L5LYOYgHh9WjXZL8NzNHA"/>
<div>
<p class="text-white font-newsreader text-sm font-semibold">Ledger History</p>
<p class="text-slate-500 text-[10px] uppercase tracking-widest">Institutional Intelligence</p>
</div>
</div>
</div>
<nav class="flex-1 overflow-y-auto font-newsreader text-sm">
<div class="bg-indigo-500/10 text-indigo-400 border-r-2 border-indigo-500 py-3 px-6 flex items-center gap-3 cursor-pointer transition-all">
<span class="material-symbols-outlined text-indigo-500">add_chart</span>
<span>New Analysis</span>
</div>
<div class="text-slate-500 py-3 px-6 hover:bg-white/5 transition-all flex items-center gap-3 cursor-pointer hover:text-white">
<span class="material-symbols-outlined">history</span>
<span>Search History</span>
</div>
<div class="text-slate-500 py-3 px-6 hover:bg-white/5 transition-all flex items-center gap-3 cursor-pointer hover:text-white">
<span class="material-symbols-outlined">monitoring</span>
<span>Fund Benchmarks</span>
</div>
<div class="text-slate-500 py-3 px-6 hover:bg-white/5 transition-all flex items-center gap-3 cursor-pointer hover:text-white">
<span class="material-symbols-outlined">account_balance</span>
<span>Sector Insights</span>
</div>
<div class="mt-8 px-6">
<p class="text-[10px] text-slate-600 uppercase tracking-widest mb-4">Recent Sessions</p>
<div class="space-y-2">
<div class="text-xs text-slate-400 hover:text-indigo-300 transition-colors truncate cursor-pointer py-1">Q3 Tech Sector Alpha...</div>
<div class="text-xs text-slate-400 hover:text-indigo-300 transition-colors truncate cursor-pointer py-1">Nifty 50 Volatility Index...</div>
<div class="text-xs text-slate-400 hover:text-indigo-300 transition-colors truncate cursor-pointer py-1">ESG Risk Parity Report...</div>
</div>
</div>
</nav>
<div class="mt-auto px-6 space-y-2">
<div class="text-slate-500 py-2 flex items-center gap-3 cursor-pointer hover:text-white transition-all text-xs">
<span class="material-symbols-outlined text-sm">cloud_done</span>
<span>System Status</span>
</div>
<div class="text-slate-500 py-2 flex items-center gap-3 cursor-pointer hover:text-white transition-all text-xs">
<span class="material-symbols-outlined text-sm">settings</span>
<span>Settings</span>
</div>
</div>
</aside>
<!-- Main Chat Canvas -->
<main class="ml-72 flex-1 flex flex-col relative overflow-hidden bg-surface-container-lowest">
<!-- Chat Header -->
<div class="px-12 py-6 flex items-center justify-between border-b border-white/5">
<div>
<h1 class="font-headline-md text-white">Equity Derivative Analysis</h1>
<p class="text-xs text-slate-500">Analyzing live order flows and structural trends</p>
</div>
<div class="flex gap-2">
<span class="px-3 py-1 bg-primary/10 border border-primary/30 rounded-full text-[10px] text-primary-fixed uppercase tracking-wider flex items-center gap-1">
<span class="material-symbols-outlined text-[12px]" style="font-variation-settings: 'FILL' 1;">verified</span> Verified Intelligence
                    </span>
<button class="p-2 glass-panel rounded-lg hover:bg-white/10 transition-colors">
<span class="material-symbols-outlined text-sm">download</span>
</button>
</div>
</div>
<!-- Messages Window -->
<div class="flex-1 overflow-y-auto px-12 py-8 space-y-12">
<!-- User Prompt -->
<div class="flex justify-end">
<div class="max-w-2xl glass-panel p-4 rounded-xl rounded-tr-none">
<p class="text-sm font-body-md text-on-surface">Can you provide a comparative analysis of the Nifty 50 performance against the Global Tech Index over the last 30 days? Focus on volatility spikes and institutional flow.</p>
<p class="text-[10px] text-slate-500 mt-2 text-right">14:02 GMT</p>
</div>
</div>
<!-- AI Response Editorial Block -->
<div class="max-w-4xl space-y-6">
<div class="flex items-start gap-4">
<div class="w-8 h-8 rounded bg-primary flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-white text-sm" style="font-variation-settings: 'FILL' 1;">terminal</span>
</div>
<div class="space-y-8 flex-1">
<!-- Narrative Text -->
<div class="editorial-border pl-6">
<h3 class="font-headline-lg text-white mb-4">Comparative Volatility and Institutional Flux</h3>
<p class="text-slate-400 leading-relaxed font-body-md mb-4">
                                    The divergence between the Nifty 50 and the Global Tech Index (GTI) has widened significantly over the trailing 30-day window. While GTI experienced a structural correction of -4.2%, the Nifty 50 maintained a relative beta-neutrality, supported by heavy domestic institutional inflows.
                                </p>
</div>
<!-- Data Art / Chart Representation -->
<div class="h-48 w-full relative flex items-end justify-between px-4">
<div class="absolute inset-0 flex items-center">
<div class="w-full h-[1px] bg-white/5"></div>
</div>
<!-- Mock Line Chart Geometric Shapes -->
<svg class="absolute inset-0 w-full h-full" preserveaspectratio="none">
<path d="M0,150 Q50,120 100,140 T200,80 T300,100 T400,60 T500,110 T600,40 T700,90 T800,20" fill="none" stroke="rgba(192, 193, 255, 0.8)" stroke-width="1.5"></path>
<path d="M0,160 Q50,150 100,155 T200,145 T300,150 T400,140 T500,145 T600,135 T700,140 T800,130" fill="none" stroke="rgba(255, 255, 255, 0.2)" stroke-width="1.5"></path>
</svg>
<div class="flex justify-between w-full text-[10px] text-slate-600 mt-auto pt-4 uppercase tracking-tighter">
<span>Aug 14</span><span>Aug 21</span><span>Aug 28</span><span>Sep 04</span><span>Sep 11</span>
</div>
</div>
<!-- Clean Data Table -->
<div class="glass-panel overflow-hidden">
<table class="w-full text-left text-[13px] font-data-mono">
<thead class="bg-white/5 text-slate-500 uppercase text-[10px] tracking-widest">
<tr>
<th class="p-4 border-b border-white/5">Metric</th>
<th class="p-4 border-b border-white/5">Nifty 50</th>
<th class="p-4 border-b border-white/5">Global Tech</th>
<th class="p-4 border-b border-white/5">Variance</th>
</tr>
</thead>
<tbody class="divide-y divide-white/5">
<tr>
<td class="p-4 text-white">Trailing Volatility (σ)</td>
<td class="p-4 text-indigo-400">12.4%</td>
<td class="p-4">18.9%</td>
<td class="p-4 text-on-error">-6.5%</td>
</tr>
<tr>
<td class="p-4 text-white">Inst. Net Flow (USD)</td>
<td class="p-4 text-indigo-400">+2.1B</td>
<td class="p-4">-1.8B</td>
<td class="p-4 text-primary">+3.9B</td>
</tr>
<tr>
<td class="p-4 text-white">Drawdown Ratio</td>
<td class="p-4 text-indigo-400">0.82</td>
<td class="p-4">1.45</td>
<td class="p-4 text-on-error">0.63</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
</div>
</div>
<!-- Input Bar -->
<div class="p-12 pt-0">
<div class="relative max-w-4xl mx-auto group">
<div class="absolute -inset-1 bg-gradient-to-r from-primary/20 to-transparent blur opacity-0 group-focus-within:opacity-100 transition duration-1000"></div>
<div class="relative glass-panel rounded-2xl flex items-center p-2">
<button class="p-2 text-slate-500 hover:text-white"><span class="material-symbols-outlined">attach_file</span></button>
<input class="flex-1 bg-transparent border-none focus:ring-0 text-sm py-4 px-4 text-on-surface placeholder:text-slate-600" placeholder="Synthesize new market intelligence..." type="text"/>
<button class="bg-primary text-on-primary-fixed w-10 h-10 rounded-xl flex items-center justify-center hover:scale-105 transition-transform">
<span class="material-symbols-outlined">arrow_upward</span>
</button>
</div>
<div class="mt-4 flex gap-4 justify-center">
<button class="text-[10px] text-slate-500 hover:text-indigo-400 transition-colors uppercase tracking-widest border-b border-transparent hover:border-indigo-400">Run Monte Carlo Simulation</button>
<button class="text-[10px] text-slate-500 hover:text-indigo-400 transition-colors uppercase tracking-widest border-b border-transparent hover:border-indigo-400">Export as PDF Terminal</button>
<button class="text-[10px] text-slate-500 hover:text-indigo-400 transition-colors uppercase tracking-widest border-b border-transparent hover:border-indigo-400">Verify Data Sources</button>
</div>
</div>
</div>
</main>
<!-- Right Side Panel (Market Data) -->
<aside class="w-80 border-l border-white/5 bg-slate-950/40 p-6 flex flex-col gap-8">
<div>
<h4 class="font-headline-md text-white text-lg mb-4">Contextual Data</h4>
<div class="space-y-4">
<div class="p-4 glass-panel rounded-xl">
<div class="flex justify-between items-center mb-2">
<span class="text-[10px] uppercase tracking-widest text-slate-500">Nifty 50</span>
<span class="text-xs text-primary">+0.42%</span>
</div>
<div class="text-xl font-data-mono text-white">24,143.85</div>
<div class="mt-3 w-full h-[2px] bg-white/5 overflow-hidden">
<div class="h-full bg-primary w-2/3"></div>
</div>
</div>
<div class="p-4 glass-panel rounded-xl">
<div class="flex justify-between items-center mb-2">
<span class="text-[10px] uppercase tracking-widest text-slate-500">VIX Index</span>
<span class="text-xs text-error">-1.20%</span>
</div>
<div class="text-xl font-data-mono text-white">13.82</div>
<div class="mt-3 w-full h-[2px] bg-white/5 overflow-hidden">
<div class="h-full bg-error w-1/4"></div>
</div>
</div>
</div>
</div>
<div class="flex-1">
<h4 class="font-headline-md text-white text-lg mb-4">Global Correlation</h4>
<div class="space-y-2">
<div class="flex items-center justify-between p-2 hover:bg-white/5 rounded-lg transition-colors cursor-pointer group">
<span class="text-xs text-slate-400 group-hover:text-white">USD/INR</span>
<span class="text-xs font-data-mono text-slate-500">83.92</span>
</div>
<div class="flex items-center justify-between p-2 hover:bg-white/5 rounded-lg transition-colors cursor-pointer group">
<span class="text-xs text-slate-400 group-hover:text-white">Brent Crude</span>
<span class="text-xs font-data-mono text-slate-500">72.41</span>
</div>
<div class="flex items-center justify-between p-2 hover:bg-white/5 rounded-lg transition-colors cursor-pointer group">
<span class="text-xs text-slate-400 group-hover:text-white">US 10Y Yield</span>
<span class="text-xs font-data-mono text-slate-500">4.18%</span>
</div>
</div>
</div>
<div class="mt-auto">
<div class="relative rounded-xl overflow-hidden aspect-video group cursor-pointer">
<img alt="Heatmap" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" data-alt="abstract financial heatmap with red and green squares and subtle digital overlay grid" src="https://lh3.googleusercontent.com/aida-public/AB6AXuB0qCfhMNXzyV63tOh9TvzOKyU2rfbHaOQi8q12kQYwF6qO04mFZT7AshWMdWZWy8Q2Ab_lY3NgVn56-YTSop9sBmmC5_pHD2nEi4Xw6IiBZqm9v9o71WHdxbRTKk9Ib93is4zV6kvVHKZKClOxAVhSwBCKg63IyX5go5EmJYRLZh6zgIIDGT4XQAZM_Qez0of0wXy-uk9T-ukVQE4vea-z8oBknOLFA8Q9xUqgXBr7SVjWSkza3CqkYJfIG3S3BPKx1dC_s6nCP7w"/>
<div class="absolute inset-0 bg-slate-950/60 flex flex-col items-center justify-center p-4">
<p class="text-[10px] uppercase tracking-[0.2em] text-indigo-400 font-bold mb-1">Live Heatmap</p>
<p class="text-[8px] text-slate-400 text-center">Sector performance overlay</p>
</div>
</div>
</div>
</aside>
</div>
<!-- Background Decoration -->
<div class="fixed top-0 right-0 w-1/2 h-1/2 bg-indigo-500/5 blur-[120px] pointer-events-none -z-10"></div>
<div class="fixed bottom-0 left-0 w-1/3 h-1/3 bg-primary/5 blur-[100px] pointer-events-none -z-10"></div>
</body></html>