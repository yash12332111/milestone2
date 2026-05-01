"use client";

import { useState, useEffect, useRef, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ChatPage() {
    return (
        <Suspense fallback={<div className="flex h-screen items-center justify-center" style={{ background: "#030f1c" }}><span className="text-slate-500 text-sm">Loading...</span></div>}>
            <ChatContent />
        </Suspense>
    );
}

function ChatContent() {
    const searchParams = useSearchParams();
    const [threads, setThreads] = useState([]);
    const [activeThreadId, setActiveThreadId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const messagesEndRef = useRef(null);
    const initialQuerySent = useRef(false);

    useEffect(() => { fetchThreads(); }, []);

    // Handle ?q= parameter - auto-send the query
    useEffect(() => {
        const q = searchParams.get("q");
        if (q && !initialQuerySent.current) {
            initialQuerySent.current = true;
            sendMessage(q);
        }
    }, [searchParams]);
    useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, loading]);

    async function fetchThreads() {
        try {
            const res = await fetch(`${API_BASE}/threads`);
            const data = await res.json();
            setThreads(data.threads || []);
        } catch (e) { console.error("Cannot connect to API", e); }
    }

    async function createThread() {
        try {
            const res = await fetch(`${API_BASE}/threads`, { method: "POST" });
            const data = await res.json();
            setActiveThreadId(data.thread_id);
            setMessages([]);
            fetchThreads();
        } catch (e) { console.error("Failed to create thread", e); }
    }

    async function switchThread(threadId) {
        setActiveThreadId(threadId);
        try {
            const res = await fetch(`${API_BASE}/threads/${threadId}/history`);
            const data = await res.json();
            setMessages(data.messages || []);
        } catch (e) { setMessages([]); }
    }

    async function deleteThread(threadId) {
        try {
            await fetch(`${API_BASE}/threads/${threadId}`, { method: "DELETE" });
            if (activeThreadId === threadId) { setActiveThreadId(null); setMessages([]); }
            fetchThreads();
        } catch (e) { console.error("Failed to delete", e); }
    }

    async function sendMessage(query) {
        if (!query.trim()) return;
        let threadId = activeThreadId;
        if (!threadId) {
            try {
                const res = await fetch(`${API_BASE}/threads`, { method: "POST" });
                const data = await res.json();
                threadId = data.thread_id;
                setActiveThreadId(threadId);
                fetchThreads();
            } catch (e) { return; }
        }
        setMessages((prev) => [...prev, { role: "user", content: query, blocked: false }]);
        setInput("");
        setLoading(true);
        try {
            const res = await fetch(`${API_BASE}/chat/${threadId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query }),
            });
            const data = await res.json();
            setMessages((prev) => [...prev, { role: "assistant", content: data.response, blocked: data.blocked, block_reason: data.block_reason }]);
            fetchThreads();
        } catch (e) {
            setMessages((prev) => [...prev, { role: "assistant", content: "Connection error. Ensure the API server is running on port 8000.", blocked: false }]);
        } finally { setLoading(false); }
    }

    function handleSubmit(e) { e.preventDefault(); sendMessage(input); }

    const examples = [
        { text: "What is the expense ratio of HDFC Large Cap Fund?", icon: "query_stats" },
        { text: "What is the minimum SIP for HDFC ELSS Tax Saver?", icon: "savings" },
        { text: "What is the exit load for HDFC Mid-Cap Fund?", icon: "trending_up" },
    ];

    return (
        <div className="flex h-screen overflow-hidden" style={{ background: "#030f1c" }}>
            {/* ═══ Left Sidebar ═══ */}
            <aside className={`h-screen ${sidebarOpen ? "w-72" : "w-0"} fixed left-0 top-0 border-r border-white/5 bg-[#040e1a]/95 backdrop-blur-2xl hidden lg:flex flex-col pt-5 pb-6 z-40 transition-all duration-300 overflow-hidden`}>
                {/* Brand */}
                <div className="px-5 mb-5">
                    <Link href="/" className="flex items-center gap-3 group">
                        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                            <span className="material-symbols-outlined text-white text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>terminal</span>
                        </div>
                        <div>
                            <p className="text-white font-[Newsreader] text-sm font-semibold tracking-tight">FundFacts AI</p>
                            <p className="text-slate-600 text-[9px] uppercase tracking-[0.2em]">Intelligence Terminal</p>
                        </div>
                    </Link>
                </div>

                <div className="px-4 mb-3">
                    <div className="glow-line w-full opacity-30"></div>
                </div>

                {/* Actions */}
                <div className="px-3">
                    <button
                        onClick={createThread}
                        className="w-full bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 py-2.5 px-4 rounded-xl flex items-center gap-3 cursor-pointer transition-all text-sm font-medium border border-indigo-500/10 hover:border-indigo-500/25"
                    >
                        <span className="material-symbols-outlined text-lg">add</span>
                        <span>New Analysis</span>
                    </button>
                </div>

                <div className="px-3 mt-2">
                    <Link href="/" className="w-full text-slate-500 hover:text-white hover:bg-white/5 py-2.5 px-4 rounded-xl flex items-center gap-3 transition-all text-sm">
                        <span className="material-symbols-outlined text-lg">arrow_back</span>
                        <span>Market Dashboard</span>
                    </Link>
                </div>

                {/* Threads */}
                <div className="mt-6 px-5 flex-1 overflow-y-auto">
                    <p className="text-[9px] text-slate-600 uppercase tracking-[0.2em] font-semibold mb-3">Recent Sessions</p>
                    <div className="space-y-0.5">
                        {threads.length === 0 && (
                            <div className="py-8 text-center">
                                <span className="material-symbols-outlined text-slate-700 text-2xl mb-2 block">forum</span>
                                <p className="text-[11px] text-slate-600">No sessions yet</p>
                            </div>
                        )}
                        {threads.map((t) => (
                            <div
                                key={t.thread_id}
                                className={`flex items-center justify-between gap-2 rounded-lg cursor-pointer transition-all py-2 px-3 ${t.thread_id === activeThreadId
                                    ? "bg-indigo-500/10 text-indigo-400 border-l-2 border-indigo-500"
                                    : "text-slate-500 hover:text-slate-300 hover:bg-white/3"
                                    }`}
                            >
                                <button onClick={() => switchThread(t.thread_id)} className="text-xs truncate flex-grow text-left cursor-pointer">
                                    {t.last_message_preview || `Session ${t.thread_id.slice(0, 8)}…`}
                                </button>
                                <button
                                    onClick={(e) => { e.stopPropagation(); deleteThread(t.thread_id); }}
                                    className="opacity-0 group-hover:opacity-100 text-slate-700 hover:text-red-400 transition-all shrink-0 cursor-pointer"
                                >
                                    <span className="material-symbols-outlined text-[14px]">close</span>
                                </button>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Status */}
                <div className="px-5 pt-4 border-t border-white/5 mt-auto">
                    <div className="flex items-center gap-2 text-[10px] text-slate-600">
                        <span className="live-dot"></span>
                        <span className="uppercase tracking-[0.15em]">Connected to Groww API</span>
                    </div>
                </div>
            </aside>

            {/* ═══ Main Chat Canvas ═══ */}
            <main className="lg:ml-72 flex-1 flex flex-col relative overflow-hidden" style={{ background: "#051424" }}>
                {/* Ambient orbs */}
                <div className="mesh-orb w-[500px] h-[500px] bg-indigo-600/5 top-[-150px] right-[-100px]" style={{ animationDelay: "0s" }}></div>
                <div className="mesh-orb w-[300px] h-[300px] bg-purple-500/4 bottom-[10%] left-[10%]" style={{ animationDelay: "10s" }}></div>

                {/* Chat Header */}
                <div className="px-8 py-4 flex items-center justify-between border-b border-white/5 shrink-0 bg-[#051424]/80 backdrop-blur-xl z-20">
                    <div className="flex items-center gap-4">
                        <button onClick={() => setSidebarOpen(!sidebarOpen)} className="lg:hidden text-slate-500 cursor-pointer">
                            <span className="material-symbols-outlined">menu</span>
                        </button>
                        <div>
                            <h1 className="font-[Newsreader] text-lg text-white tracking-tight">Intelligence Terminal</h1>
                            <p className="text-[10px] text-slate-600 uppercase tracking-[0.15em]">Real-time verified fund data</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-500/8 border border-indigo-500/15 rounded-full text-[10px] text-indigo-400 uppercase tracking-wider">
                            <span className="material-symbols-outlined text-[11px]" style={{ fontVariationSettings: "'FILL' 1" }}>verified</span>
                            Verified Source
                        </span>
                        <Link href="/" className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center hover:bg-white/10 transition-colors text-slate-500 hover:text-white">
                            <span className="material-symbols-outlined text-sm">home</span>
                        </Link>
                    </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto px-6 md:px-12 py-8 space-y-8 relative z-10">
                    {/* Empty State */}
                    {messages.length === 0 && !loading && (
                        <div className="flex flex-col items-center justify-center h-full text-center animate-fade-up">
                            <div className="relative mb-8">
                                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-600/20 to-purple-600/10 flex items-center justify-center border border-indigo-500/20">
                                    <span className="material-symbols-outlined text-indigo-400 text-3xl">terminal</span>
                                </div>
                                <div className="absolute -top-1 -right-1 w-5 h-5 bg-indigo-500 rounded-full flex items-center justify-center badge-pulse">
                                    <span className="material-symbols-outlined text-white text-[10px]" style={{ fontVariationSettings: "'FILL' 1" }}>bolt</span>
                                </div>
                            </div>
                            <h2 className="font-[Newsreader] text-3xl md:text-4xl text-white mb-3">Intelligence Terminal</h2>
                            <p className="text-slate-500 mb-10 max-w-md text-sm leading-relaxed">
                                Ask factual questions about HDFC mutual fund schemes. All data is verified against Groww.
                            </p>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 w-full max-w-3xl">
                                {examples.map((ex, i) => (
                                    <button
                                        key={i}
                                        onClick={() => sendMessage(ex.text)}
                                        className="p-5 glass-panel-hover rounded-2xl flex flex-col items-start gap-3 text-left cursor-pointer group"
                                    >
                                        <div className="w-9 h-9 rounded-lg bg-indigo-500/10 flex items-center justify-center group-hover:bg-indigo-500/20 transition-colors">
                                            <span className="material-symbols-outlined text-indigo-400 text-sm">{ex.icon}</span>
                                        </div>
                                        <p className="text-xs text-slate-400 group-hover:text-slate-200 leading-relaxed transition-colors">{ex.text}</p>
                                    </button>
                                ))}
                            </div>
                            <p className="text-[10px] text-slate-700 mt-10 flex items-center gap-1.5">
                                <span className="material-symbols-outlined text-[12px]">info</span>
                                Facts-only. No investment advice. All data sourced from Groww.
                            </p>
                        </div>
                    )}

                    {/* Message Bubbles */}
                    {messages.map((msg, idx) => (
                        <div key={idx} className="animate-fade-up" style={{ animationDelay: "0.05s" }}>
                            {msg.role === "user" ? (
                                <div className="flex justify-end">
                                    <div className="max-w-2xl bg-indigo-600/15 border border-indigo-500/20 p-4 rounded-2xl rounded-tr-sm">
                                        <p className="text-sm text-slate-200 leading-relaxed">{msg.content}</p>
                                    </div>
                                </div>
                            ) : (
                                <div className="max-w-4xl">
                                    <div className="flex items-start gap-4">
                                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-600 to-indigo-500 flex items-center justify-center shrink-0 shadow-lg shadow-indigo-500/20">
                                            <span className="material-symbols-outlined text-white text-xs" style={{ fontVariationSettings: "'FILL' 1" }}>terminal</span>
                                        </div>
                                        <div className="flex-1 pt-0.5">
                                            {msg.blocked ? (
                                                <div className="bg-red-500/8 border border-red-500/15 rounded-2xl p-5">
                                                    <div className="flex items-start gap-3">
                                                        <span className="material-symbols-outlined text-red-400 text-lg shrink-0">warning</span>
                                                        <p className="text-sm text-red-300/80 leading-relaxed">{msg.content}</p>
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="editorial-border">
                                                    {(() => {
                                                        const parts = msg.content.split("\n\nSource:");
                                                        return (
                                                            <>
                                                                <p className="text-sm text-slate-300 leading-[1.8]">{parts[0]}</p>
                                                                {parts[1] && (
                                                                    <div className="mt-4 inline-flex items-center gap-2 px-3 py-1.5 bg-indigo-500/8 border border-indigo-500/15 rounded-full text-[10px] text-indigo-400">
                                                                        <span className="material-symbols-outlined text-[12px]" style={{ fontVariationSettings: "'FILL' 1" }}>verified</span>
                                                                        Source:{parts[1]}
                                                                    </div>
                                                                )}
                                                            </>
                                                        );
                                                    })()}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}

                    {/* Loading */}
                    {loading && (
                        <div className="max-w-4xl animate-fade-up">
                            <div className="flex items-start gap-4">
                                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-600 to-indigo-500 flex items-center justify-center shrink-0 shadow-lg shadow-indigo-500/20">
                                    <span className="material-symbols-outlined text-white text-xs">smart_toy</span>
                                </div>
                                <div className="editorial-border flex items-center gap-2 py-2">
                                    <div className="w-2 h-2 bg-indigo-400 rounded-full typing-dot"></div>
                                    <div className="w-2 h-2 bg-indigo-400 rounded-full typing-dot"></div>
                                    <div className="w-2 h-2 bg-indigo-400 rounded-full typing-dot"></div>
                                    <span className="text-[10px] text-slate-600 ml-2">Synthesizing intelligence...</span>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Bar */}
                <div className="px-6 md:px-12 pb-6 pt-2 shrink-0 relative z-10">
                    <form onSubmit={handleSubmit} className="relative max-w-4xl mx-auto group">
                        <div className="absolute -inset-[2px] rounded-2xl bg-gradient-to-r from-indigo-500/25 via-purple-500/15 to-indigo-500/25 opacity-0 group-focus-within:opacity-100 transition-opacity duration-700 blur-sm"></div>
                        <div className="relative glass-panel rounded-2xl flex items-center p-2 border-white/8">
                            <div className="pl-3">
                                <span className="material-symbols-outlined text-slate-600 text-lg">edit_note</span>
                            </div>
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                disabled={loading}
                                className="flex-1 bg-transparent border-none focus:ring-0 text-sm py-3.5 px-3 text-white placeholder:text-slate-600 outline-none"
                                placeholder="Ask about fund facts, expense ratios, or SIP details..."
                            />
                            <button
                                type="submit"
                                disabled={loading || !input.trim()}
                                className="bg-gradient-to-r from-indigo-600 to-indigo-500 text-white w-9 h-9 rounded-xl flex items-center justify-center hover:shadow-lg hover:shadow-indigo-500/30 transition-all disabled:opacity-30 disabled:shadow-none cursor-pointer"
                            >
                                <span className="material-symbols-outlined text-sm">arrow_upward</span>
                            </button>
                        </div>
                        <div className="mt-3 flex gap-3 justify-center flex-wrap">
                            {examples.map((ex, i) => (
                                <button
                                    type="button"
                                    key={i}
                                    onClick={() => sendMessage(ex.text)}
                                    className="text-[9px] text-slate-600 hover:text-indigo-400 transition-all uppercase tracking-[0.15em] hover:tracking-[0.2em] cursor-pointer"
                                >
                                    {ex.text.length > 35 ? ex.text.slice(0, 35) + "…" : ex.text}
                                </button>
                            ))}
                        </div>
                    </form>
                </div>
            </main>

            {/* ═══ Right Panel ═══ */}
            <aside className="hidden xl:flex w-72 border-l border-white/5 flex-col gap-6 overflow-y-auto p-5" style={{ background: "#040e1a" }}>
                <div>
                    <div className="flex items-center justify-between mb-4">
                        <h4 className="text-[10px] text-slate-500 uppercase tracking-[0.2em] font-semibold">Market Pulse</h4>
                        <span className="live-dot"></span>
                    </div>
                    <div className="space-y-3">
                        <div className="p-4 glass-panel rounded-xl">
                            <div className="flex justify-between items-center mb-1">
                                <span className="text-[10px] uppercase tracking-[0.15em] text-slate-600">Nifty 50</span>
                                <span className="text-[11px] text-emerald-400 font-mono">+0.42%</span>
                            </div>
                            <div className="text-lg text-white font-mono font-medium number-highlight">24,143.85</div>
                            <div className="mt-3 w-full h-1 bg-white/5 rounded-full overflow-hidden">
                                <div className="h-full bg-gradient-to-r from-indigo-600 to-indigo-400 w-2/3 rounded-full"></div>
                            </div>
                        </div>
                        <div className="p-4 glass-panel rounded-xl">
                            <div className="flex justify-between items-center mb-1">
                                <span className="text-[10px] uppercase tracking-[0.15em] text-slate-600">VIX</span>
                                <span className="text-[11px] text-red-400 font-mono">-1.20%</span>
                            </div>
                            <div className="text-lg text-white font-mono font-medium">13.82</div>
                            <div className="mt-3 w-full h-1 bg-white/5 rounded-full overflow-hidden">
                                <div className="h-full bg-gradient-to-r from-red-600 to-red-400 w-1/4 rounded-full"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="glow-line w-full opacity-20"></div>

                <div>
                    <h4 className="text-[10px] text-slate-500 uppercase tracking-[0.2em] font-semibold mb-4">Global Rates</h4>
                    <div className="space-y-1">
                        {[
                            { label: "USD/INR", val: "83.92", change: "+0.08%" },
                            { label: "Brent Crude", val: "72.41", change: "-0.34%" },
                            { label: "US 10Y", val: "4.18%", change: "+0.02%" },
                        ].map(item => (
                            <div key={item.label} className="flex items-center justify-between p-2.5 hover:bg-white/3 rounded-lg transition-colors cursor-pointer group">
                                <span className="text-xs text-slate-500 group-hover:text-slate-300 transition-colors">{item.label}</span>
                                <div className="text-right">
                                    <span className="text-xs font-mono text-slate-400 block">{item.val}</span>
                                    <span className={`text-[9px] font-mono ${item.change.startsWith("+") ? "text-emerald-500" : "text-red-500"}`}>{item.change}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="glow-line w-full opacity-20"></div>

                <div>
                    <h4 className="text-[10px] text-slate-500 uppercase tracking-[0.2em] font-semibold mb-4">Data Coverage</h4>
                    <div className="space-y-3">
                        {[
                            { label: "HDFC Mutual Fund", pct: 100 },
                            { label: "Groww Verified", pct: 100 },
                            { label: "Real-time NAV", pct: 87 },
                        ].map(item => (
                            <div key={item.label}>
                                <div className="flex justify-between items-center mb-1.5">
                                    <span className="text-[10px] text-slate-500">{item.label}</span>
                                    <span className="text-[10px] font-mono text-slate-600">{item.pct}%</span>
                                </div>
                                <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                                    <div className="h-full bg-gradient-to-r from-indigo-600 to-indigo-400 rounded-full" style={{ width: `${item.pct}%` }}></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </aside>
        </div>
    );
}
