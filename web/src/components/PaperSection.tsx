import { motion } from 'framer-motion'
import { ExternalLink } from 'lucide-react'

export function PaperSection() {
  return (
    <section
      id="paper"
      className="scroll-mt-20 border-t border-cyber-border bg-cyber-surface/40 px-6 py-16 md:py-20"
    >
      <div className="mx-auto max-w-3xl text-center">
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-xl font-bold text-slate-100 md:text-2xl"
        >
          IEEE paper &amp; artifacts
        </motion.h2>
        <p className="mt-3 text-sm text-slate-400 md:text-base">
          When your DOI is available, link it here. Until then, the repository README documents
          architecture, cost simulation, and live AWS validation for the Budget-Aware AI Squad.
        </p>
        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <a
            href="https://github.com/SiD-array/Autonomous-Cloud-Governance"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-lg border border-cyan-500/30 bg-cyan-500/5 px-6 py-3 text-sm font-semibold text-cyan-200 transition hover:bg-cyan-500/10"
          >
            <ExternalLink className="size-4" aria-hidden />
            Open GitHub repository
          </a>
          <a
            href="#evidence"
            className="text-sm font-medium text-slate-500 underline-offset-4 hover:text-slate-300 hover:underline"
          >
            Jump to ledger evidence
          </a>
        </div>
      </div>
    </section>
  )
}
