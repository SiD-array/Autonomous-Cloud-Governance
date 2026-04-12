import { useEffect, useState } from 'react'
import { motion, useSpring, useTransform } from 'framer-motion'
import { Activity, DollarSign, Shield } from 'lucide-react'
import { useInViewOnce } from '../hooks/useInViewOnce'

function OdometerValue({
  value,
  decimals,
  suffix,
  enabled,
}: {
  value: number
  decimals: number
  suffix: string
  enabled: boolean
}) {
  const spring = useSpring(0, { stiffness: 90, damping: 28 })
  const display = useTransform(spring, (v) => {
    const n = decimals > 0 ? v.toFixed(decimals) : Math.round(v).toString()
    return `${n}${suffix}`
  })
  const [text, setText] = useState('0' + suffix)

  useEffect(() => {
    const unsub = display.on('change', (v) => setText(v))
    return () => unsub()
  }, [display])

  useEffect(() => {
    if (enabled) spring.set(value)
  }, [enabled, spring, value])

  return <span className="font-mono tabular-nums tracking-tight">{text}</span>
}

export function GovernanceMetrics() {
  const { ref, inView } = useInViewOnce()

  return (
    <section ref={ref} className="border-b border-cyber-border px-6 py-16 md:py-24">
      <div className="mx-auto max-w-6xl">
        <h2 className="text-center text-2xl font-bold tracking-tight text-slate-100 md:text-3xl">
          Governance metrics
        </h2>
        <p className="mx-auto mt-3 max-w-2xl text-center text-slate-400">
          Odometer-style telemetry from a representative mesh pass ($0.024 saved vs $0.005 spent).
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-3">
          <motion.article
            initial={{ opacity: 0, y: 20 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5, delay: 0 }}
            className="rounded-xl border border-cyber-border bg-gradient-to-b from-cyber-elevated to-cyber-void p-6 shadow-lg shadow-emerald-950/20"
          >
            <div className="flex items-center gap-2 text-emerald-glow">
              <DollarSign className="size-5" aria-hidden />
              <span className="text-xs font-semibold uppercase tracking-wider">Savings rate</span>
            </div>
            <p className="mt-4 text-4xl font-bold text-slate-50 md:text-5xl">
              <OdometerValue value={80} decimals={0} suffix="%" enabled={inView} />
            </p>
            <p className="mt-2 text-sm text-slate-500">≈ $0.024 avoided vs $0.005 deployed</p>
          </motion.article>

          <motion.article
            initial={{ opacity: 0, y: 20 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="rounded-xl border border-cyber-border bg-gradient-to-b from-cyber-elevated to-cyber-void p-6 shadow-lg shadow-cyan-950/20"
          >
            <div className="flex items-center gap-2 text-cyan-bright">
              <Shield className="size-5" aria-hidden />
              <span className="text-xs font-semibold uppercase tracking-wider">Governance overhead</span>
            </div>
            <p className="mt-4 text-4xl font-bold text-slate-50 md:text-5xl">
              <span className="text-slate-500">&lt; </span>
              <OdometerValue value={0.01} decimals={2} suffix="%" enabled={inView} />
            </p>
            <p className="mt-2 text-sm text-slate-500">Accountant handshake — sub-millisecond path</p>
          </motion.article>

          <motion.article
            initial={{ opacity: 0, y: 20 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="rounded-xl border border-cyber-border bg-gradient-to-b from-cyber-elevated to-cyber-void p-6 shadow-lg shadow-slate-900/40"
          >
            <div className="flex items-center gap-2 text-slate-300">
              <Activity className="size-5" aria-hidden />
              <span className="text-xs font-semibold uppercase tracking-wider">Response accuracy</span>
            </div>
            <p className="mt-4 text-4xl font-bold text-slate-50 md:text-5xl">
              <OdometerValue value={100} decimals={0} suffix="%" enabled={inView} />
            </p>
            <p className="mt-2 text-sm text-slate-500">Task output validated after routing events</p>
          </motion.article>
        </div>
      </div>
    </section>
  )
}
