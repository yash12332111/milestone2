"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Header() {
    const pathname = usePathname();

    const links = [
        { href: "/", label: "Market" },
        { href: "/chat", label: "Intelligence" },
    ];

    return (
        <header className="sticky top-0 w-full z-50 flex items-center justify-between px-6 sm:px-8 py-4 bg-[#051424]/70 backdrop-blur-2xl border-b border-white/5">
            <div className="flex items-center gap-8">
                <Link href="/" className="flex items-center gap-3 group">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:shadow-indigo-500/40 transition-shadow">
                        <span className="material-symbols-outlined text-white text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>terminal</span>
                    </div>
                    <span className="font-[Newsreader] text-lg font-semibold tracking-tight text-white">FundFacts AI</span>
                </Link>
                <nav className="hidden md:flex items-center gap-1">
                    {links.map((link) => (
                        <Link
                            key={link.href}
                            href={link.href}
                            className={`px-4 py-2 rounded-lg text-sm transition-all ${pathname === link.href
                                    ? "text-white bg-white/5 font-medium"
                                    : "text-slate-500 hover:text-slate-300 hover:bg-white/3"
                                }`}
                        >
                            {link.label}
                        </Link>
                    ))}
                </nav>
            </div>
            <div className="flex items-center gap-3">
                <div className="relative cursor-pointer group">
                    <span className="material-symbols-outlined text-slate-500 group-hover:text-indigo-400 transition-colors text-xl">notifications</span>
                    <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-indigo-500 rounded-full badge-pulse"></span>
                </div>
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-slate-700 to-slate-600 flex items-center justify-center cursor-pointer hover:from-indigo-600 hover:to-indigo-500 transition-all">
                    <span className="material-symbols-outlined text-white text-sm">person</span>
                </div>
            </div>
        </header>
    );
}
