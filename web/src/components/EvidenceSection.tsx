import { motion } from 'framer-motion'
import { FileText } from 'lucide-react'

const LEDGER_LINES = [
  'FINAL_FINANCIAL_LEDGER — session_id=acg-mesh-7f3a',
  '────────────────────────────────────────────────────',
  'agent.Researcher    | op=llm_infer_cloud | debit=$0.0080 | cum=$0.0080',
  'agent.Researcher    | op=s3_read         | debit=$0.0000 | cum=$0.0080',
  'router.guard        | event=complexity_scan | tier=LOW | action=ROUTE_FRUGAL',
  'agent.Writer        | op=llm_infer_local | debit=$0.0000 | cum=$0.0080',
  'accountant.reserve  | floor=$0.0010     | status=HELD',
  'accountant.close    | remainder=$0.0010 | breaker=CLOSED',
  'savings.vs_premium  | delta=$0.0240     | rate=~80%',
  '────────────────────────────────────────────────────',
  'PROOF_OF_EXECUTION — hash=sha256:4b2c…9e1f  | verified=true',
]

export function EvidenceSection() {
  return (
    <section id="evidence" className="scroll-mt-20 px-6 py-16 md:py-24">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 flex items-center gap-3">
          <FileText className="size-6 text-cyan-bright" aria-hidden />
          <h2 className="text-2xl font-bold tracking-tight text-slate-100 md:text-3xl">
            Proof of execution
          </h2>
        </div>
        <p className="mb-8 max-w-2xl text-slate-400">
          Stylized final ledger excerpt from a budget-aware pass: cloud spend on the Researcher,
          zero-cost local inference on the Writer after downgrade, and an explicit reserve preserved
          by the circuit breaker.
        </p>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.5 }}
          className="overflow-hidden rounded-xl border border-emerald-500/20 bg-[#060a0d] shadow-[0_0_40px_-12px_rgba(52,211,153,0.35)]"
        >
          <div className="flex items-center gap-2 border-b border-cyber-border bg-cyber-elevated px-4 py-2">
            <span className="size-2 rounded-full bg-emerald-500" />
            <span className="size-2 rounded-full bg-amber-400" />
            <span className="size-2 rounded-full bg-rose-400" />
            <span className="ml-3 font-mono text-[10px] uppercase tracking-widest text-slate-500">
              final_financial_ledger.log
            </span>
          </div>
          <pre className="max-h-[360px] overflow-auto p-4 font-mono text-[10px] leading-relaxed text-slate-300 md:text-xs">
            {LEDGER_LINES.map((line, i) => (
              <motion.span
                key={i}
                initial={{ opacity: 0, x: -4 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.04 }}
                className="block"
              >
                <span className="text-slate-600">{String(i + 1).padStart(2, '0')} │ </span>
                {line.includes('savings') || line.includes('PROOF') ? (
                  <span className="text-emerald-glow">{line}</span>
                ) : line.includes('router') || line.includes('ROUTE') ? (
                  <span className="text-cyan-bright">{line}</span>
                ) : line.includes('debit') ? (
                  <span className="text-slate-400">{line}</span>
                ) : (
                  <span className="text-slate-500">{line}</span>
                )}
              </motion.span>
            ))}
          </pre>
        </motion.div>
      </div>
    </section>
  )
}
