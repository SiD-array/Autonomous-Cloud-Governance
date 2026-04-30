import { useCallback, useEffect, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Cpu, DollarSign, RefreshCw, Shield } from 'lucide-react'

type LogLevel = 'info' | 'warn' | 'error' | 'ok' | 'route'

type BudgetMode = 'standard' | 'aware'

type LogLine = { t: number; level: LogLevel; text: string }

const STANDARD_SCRIPT: LogLine[] = [
  { t: 0, level: 'info', text: '[00:00.000] mesh_init — daily_ceiling=$0.0300' },
  { t: 400, level: 'info', text: '[AGENT:Researcher] llm.request — forecast $0.0082 (PREMIUM)' },
  { t: 750, level: 'ok', text: '[BudgetGuard] clearance GRANTED — CtC within envelope' },
  { t: 1100, level: 'warn', text: '[AGENT:Researcher] recursive_self_delegate depth=8 → depth=24' },
  { t: 1500, level: 'warn', text: '[BudgetGuard] runaway_loop_detected — token storm +420% vs. prior' },
  { t: 1900, level: 'error', text: '[Accountant] CIRCUIT_BREAKER → OPEN — projected_spend > remainder' },
  { t: 2300, level: 'error', text: '[MESH] execution HALTED — status=BUDGET_EXHAUSTED' },
]

const AWARE_SCRIPT: LogLine[] = [
  { t: 0, level: 'info', text: '[00:00.000] mesh_init — daily_ceiling=$0.0300 | proactive_router=ON' },
  { t: 380, level: 'info', text: '[AGENT:Researcher] s3.read + llm.infer — settled $0.0080 (cloud)' },
  { t: 820, level: 'ok', text: '[Accountant] ledger_commit — remaining=$0.0220' },
  { t: 1180, level: 'warn', text: '[ROUTER] ⚠ Downgrade — Writer task LOW_COMPLEXITY (format/summarize)' },
  { t: 1550, level: 'route', text: '[BudgetGuard] dynamic_route → Writer@LOCAL_FRUGAL ($0.0000 est.)' },
  { t: 1920, level: 'ok', text: '[AGENT:Writer] ollama/llama3.1 — inference_complete latency=412ms' },
  { t: 2280, level: 'ok', text: '[Accountant] circuit_breaker=CLOSED — reserve_preserved=$0.0010' },
  { t: 2650, level: 'ok', text: '[MESH] SUCCESS — fiscal_boundary_respected | savings_vs_premium ~80%' },
]

const LEVEL_STYLES: Record<LogLevel, string> = {
  info: 'text-slate-400',
  warn: 'text-amber-400',
  error: 'text-rose-400',
  ok: 'text-emerald-glow',
  route: 'text-cyan-bright',
}

function budgetKeyframes(mode: BudgetMode): { time: number; value: number }[] {
  if (mode === 'standard') {
    return [
      { time: 0, value: 0.03 },
      { time: 900, value: 0.018 },
      { time: 1600, value: 0.006 },
      { time: 2100, value: 0.0 },
    ]
  }
  return [
    { time: 0, value: 0.03 },
    { time: 700, value: 0.022 },
    { time: 1400, value: 0.012 },
    { time: 2200, value: 0.001 },
  ]
}

export function SimulationDashboard() {
  const [mode, setMode] = useState<BudgetMode>('aware')
  const [logs, setLogs] = useState<LogLine[]>([])
  const [budget, setBudget] = useState(0.03)
  const [running, setRunning] = useState(false)
  const [phase, setPhase] = useState<'idle' | 'fail' | 'ok'>('idle')
  const terminalRef = useRef<HTMLDivElement>(null)
  const simAbortRef = useRef<AbortController | null>(null)

  const scrollTerminal = useCallback(() => {
    const el = terminalRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [])

  const runSimulation = useCallback(
    (nextMode: BudgetMode) => {
      simAbortRef.current?.abort()
      const ac = new AbortController()
      simAbortRef.current = ac
      const { signal } = ac

      setRunning(true)
      setLogs([])
      setPhase('idle')
      const script = nextMode === 'standard' ? STANDARD_SCRIPT : AWARE_SCRIPT
      const keyframes = budgetKeyframes(nextMode)
      let budgetIdx = 0
      setBudget(keyframes[0].value)

      const start = performance.now()

      function tick(now: number) {
        if (signal.aborted) return
        const elapsed = now - start

        while (budgetIdx < keyframes.length - 1 && elapsed >= keyframes[budgetIdx + 1].time) {
          budgetIdx++
        }
        const a = keyframes[budgetIdx]
        const b = keyframes[Math.min(budgetIdx + 1, keyframes.length - 1)]
        let bv = a.value
        if (b.time > a.time && elapsed < b.time) {
          const u = (elapsed - a.time) / (b.time - a.time)
          bv = a.value + (b.value - a.value) * u
        } else if (elapsed >= b.time) {
          bv = b.value
        }
        setBudget(Math.max(0, bv))

        setLogs((prev) => {
          const next = script.filter((l) => l.t <= elapsed)
          if (next.length === prev.length && next.every((x, i) => x === prev[i])) return prev
          return next
        })

        scrollTerminal()

        if (signal.aborted) return
        if (elapsed < script[script.length - 1].t + 450) {
          requestAnimationFrame(tick)
        } else {
          setRunning(false)
          setPhase(nextMode === 'standard' ? 'fail' : 'ok')
        }
      }

      requestAnimationFrame(tick)
    },
    [scrollTerminal]
  )

  useEffect(() => {
    runSimulation(mode)
    return () => {
      simAbortRef.current?.abort()
    }
  }, [mode, runSimulation])

  const pct = Math.min(100, (budget / 0.03) * 100)
  const gaugeColor =
    phase === 'fail' || (running && budget < 0.004 && mode === 'standard')
      ? 'from-rose-500 to-orange-600'
      : running && budget < 0.012
        ? 'from-amber-400 to-amber-600'
        : 'from-emerald-500 to-cyan-500'

  return (
    <section
      id="simulation"
      className="scroll-mt-20 border-b border-cyber-border bg-cyber-surface/50 px-6 py-16 md:py-24"
    >
      <div className="mx-auto max-w-6xl">
        <div className="mb-10 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-slate-100 md:text-3xl">
              Interactive simulation
            </h2>
            <p className="mt-2 max-w-xl text-slate-400">
              Live execution log versus budget telemetry. Toggle modes to feel the mesh fail in
              standard conditions — then recover under budget-aware governance.
            </p>
            <p className="mt-2 text-xs text-slate-500">
              Demonstration view: timeline, metrics, and ledger lines are illustrative product
              simulation.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
              Budget mode
            </span>
            <div className="flex rounded-lg border border-cyber-border bg-cyber-void p-1">
              <button
                type="button"
                onClick={() => setMode('standard')}
                className={`rounded-md px-4 py-2 text-sm font-semibold transition ${
                  mode === 'standard'
                    ? 'bg-rose-500/20 text-rose-300'
                    : 'text-slate-500 hover:text-slate-300'
                }`}
              >
                Standard
              </button>
              <button
                type="button"
                onClick={() => setMode('aware')}
                className={`rounded-md px-4 py-2 text-sm font-semibold transition ${
                  mode === 'aware'
                    ? 'bg-emerald-500/20 text-emerald-300'
                    : 'text-slate-500 hover:text-slate-300'
                }`}
              >
                Budget-aware
              </button>
            </div>
            <button
              type="button"
              onClick={() => runSimulation(mode)}
              disabled={running}
              className="inline-flex items-center gap-2 rounded-lg border border-cyber-border px-3 py-2 text-sm text-slate-300 transition hover:border-cyan-500/40 disabled:opacity-40"
            >
              <RefreshCw className={`size-4 ${running ? 'animate-spin' : ''}`} aria-hidden />
              Replay
            </button>
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Terminal */}
          <motion.div
            layout
            className="flex min-h-[340px] flex-col overflow-hidden rounded-xl border border-cyber-border bg-cyber-void shadow-xl shadow-black/40"
          >
            <div className="flex items-center justify-between border-b border-cyber-border bg-cyber-elevated px-4 py-2">
              <div className="flex items-center gap-2 text-xs font-medium text-slate-400">
                <Cpu className="size-3.5 text-cyan-400" aria-hidden />
                execution.log
              </div>
              <motion.div
                className="flex items-center gap-1.5 text-[10px] font-mono uppercase tracking-wider"
                animate={{
                  color: phase === 'fail' ? '#fb7185' : phase === 'ok' ? '#34d399' : '#64748b',
                }}
              >
                <motion.span
                  animate={{
                    scale: running ? [1, 1.2, 1] : 1,
                    opacity: running ? [1, 0.6, 1] : 1,
                  }}
                  transition={{ repeat: running ? Infinity : 0, duration: 1.2 }}
                  className="inline-block size-1.5 rounded-full bg-current"
                />
                {running ? 'streaming' : phase === 'fail' ? 'failed' : phase === 'ok' ? 'stable' : 'idle'}
              </motion.div>
            </div>
            <div
              ref={terminalRef}
              className="font-mono flex-1 overflow-y-auto p-4 text-[11px] leading-relaxed md:text-xs"
            >
              <AnimatePresence mode="popLayout">
                {logs.map((line, i) => (
                  <motion.div
                    key={`${line.t}-${i}`}
                    initial={{ opacity: 0, x: -6 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2 }}
                    className={`mb-1 border-l-2 border-transparent pl-2 ${LEVEL_STYLES[line.level]}`}
                    style={{
                      borderLeftColor:
                        line.level === 'error'
                          ? 'rgba(251,113,133,0.5)'
                          : line.level === 'route'
                            ? 'rgba(34,211,238,0.5)'
                            : 'transparent',
                    }}
                  >
                    {line.text}
                  </motion.div>
                ))}
              </AnimatePresence>
              {logs.length === 0 && (
                <span className="text-slate-600">Waiting for telemetry…</span>
              )}
            </div>
          </motion.div>

          {/* Gauge */}
          <div className="flex min-h-[340px] flex-col justify-between rounded-xl border border-cyber-border bg-cyber-void p-6 shadow-xl shadow-black/40">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2 text-slate-400">
                  <DollarSign className="size-4 text-emerald-glow" aria-hidden />
                  <span className="text-xs font-semibold uppercase tracking-wider">Live budget</span>
                </div>
                <motion.p
                  key={budget.toFixed(4)}
                  initial={{ scale: 1.02 }}
                  animate={{ scale: 1 }}
                  className="mt-3 font-mono text-4xl font-bold tracking-tight text-slate-100 md:text-5xl"
                >
                  ${budget.toFixed(4)}
                </motion.p>
                <p className="mt-1 text-xs text-slate-500">Remaining of $0.0300 daily envelope</p>
              </div>
              <motion.div
                animate={
                  mode === 'aware' && phase === 'ok'
                    ? { rotate: [0, -6, 6, 0], scale: [1, 1.05, 1] }
                    : mode === 'standard' && phase === 'fail'
                      ? { x: [0, -4, 4, -4, 0] }
                      : {}
                }
                transition={{ duration: 0.5 }}
              >
                <Shield
                  className={`size-12 md:size-14 ${
                    phase === 'fail' ? 'text-rose-400' : phase === 'ok' ? 'text-emerald-glow' : 'text-slate-600'
                  }`}
                  aria-hidden
                />
              </motion.div>
            </div>

            <div className="mt-8">
              <div className="mb-2 flex justify-between text-[10px] uppercase tracking-wider text-slate-500">
                <span>Depleted</span>
                <span>Headroom</span>
              </div>
              <div className="h-3 overflow-hidden rounded-full bg-cyber-elevated ring-1 ring-cyber-border">
                <motion.div
                  className={`h-full rounded-full bg-gradient-to-r ${gaugeColor}`}
                  animate={{ width: `${pct}%` }}
                  transition={{ type: 'spring', stiffness: 120, damping: 18 }}
                />
              </div>
            </div>

            <motion.div
              className="mt-6 rounded-lg border border-cyber-border bg-cyber-elevated/80 p-4"
              animate={{
                borderColor:
                  phase === 'fail'
                    ? 'rgba(251,113,133,0.35)'
                    : phase === 'ok'
                      ? 'rgba(52,211,153,0.35)'
                      : 'rgba(30,45,61,1)',
              }}
            >
              <p className="text-xs font-medium text-slate-300">
                {mode === 'standard'
                  ? 'Standard mesh: recursive chatter consumes the envelope; the circuit breaker trips only after projected ruin.'
                  : 'Budget-aware mesh: the Accountant preserves a hard reserve; the Guard downgrades the Writer to local inference before the cliff.'}
              </p>
              <motion.div
                className="mt-3 flex items-center gap-2 text-[10px] font-mono text-cyan-400/90"
                animate={{ opacity: running ? [0.5, 1, 0.5] : 0.7 }}
                transition={{ repeat: running ? Infinity : 0, duration: 1.5 }}
              >
                <span className="inline-block size-1.5 rounded-full bg-cyan-400" />
                routing_layer / fiscal_telemetry
              </motion.div>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  )
}
