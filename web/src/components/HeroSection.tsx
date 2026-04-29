import { motion } from 'framer-motion'
import { Activity, Shield } from 'lucide-react'

const IEEE_PAPER_URL =
  'https://github.com/SiD-array/Autonomous-Cloud-Governance/blob/main/Final%20Report.pdf'

export function HeroSection() {
  return (
    <header className="relative overflow-hidden border-b border-cyber-border bg-gradient-to-b from-cyber-surface to-cyber-void px-6 py-20 md:py-28">
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.07]"
        style={{
          backgroundImage: `linear-gradient(rgba(34,211,238,0.3) 1px, transparent 1px),
            linear-gradient(90deg, rgba(52,211,153,0.25) 1px, transparent 1px)`,
          backgroundSize: '48px 48px',
        }}
      />
      <motion.div
        className="pointer-events-none absolute -right-20 top-1/4 h-96 w-96 rounded-full bg-cyan-500/10 blur-[100px]"
        animate={{ opacity: [0.4, 0.7, 0.4], scale: [1, 1.08, 1] }}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
      />
      <motion.div
        className="pointer-events-none absolute -left-16 bottom-0 h-72 w-72 rounded-full bg-emerald-500/10 blur-[90px]"
        animate={{ opacity: [0.35, 0.65, 0.35] }}
        transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
      />

      <div className="relative mx-auto max-w-4xl text-center">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-6 inline-flex items-center gap-2 rounded-full border border-cyan-500/25 bg-cyan-500/5 px-4 py-1.5 text-xs font-medium uppercase tracking-widest text-cyan-400"
        >
          <Shield className="size-3.5" aria-hidden />
          Cyber-FinOps · Agentic era
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, delay: 0.08 }}
          className="text-balance text-3xl font-bold leading-tight tracking-tight text-slate-100 md:text-5xl md:leading-[1.1]"
        >
          Autonomous Cloud Governance for the Agentic Era.
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, delay: 0.16 }}
          className="mx-auto mt-6 max-w-2xl text-pretty text-base text-slate-400 md:text-lg"
        >
          Preventing fiscal volatility in multi-agent systems through real-time circuit breakers
          and proactive dynamic routing.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, delay: 0.24 }}
          className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row"
        >
          <a
            href="#simulation"
            className="group inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-emerald-600 to-cyan-600 px-8 py-3.5 text-sm font-semibold text-white shadow-lg shadow-cyan-900/30 transition hover:brightness-110"
          >
            <Activity className="size-4 transition group-hover:scale-110" aria-hidden />
            Watch Simulation
          </a>
          <a
            href={IEEE_PAPER_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center rounded-lg border border-cyber-border bg-cyber-elevated px-8 py-3.5 text-sm font-semibold text-slate-200 transition hover:border-cyan-500/40 hover:text-cyan-200"
          >
            Read IEEE Paper
          </a>
        </motion.div>
      </div>
    </header>
  )
}
