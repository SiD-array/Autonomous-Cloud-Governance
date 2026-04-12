import { useState } from 'react'
import { motion } from 'framer-motion'

const NODES = [
  { id: 'user', label: 'User', sub: 'Intent', x: 60, y: 140 },
  { id: 'guard', label: 'Budget Guard', sub: 'Interceptor', x: 220, y: 60 },
  { id: 'accountant', label: 'Accountant', sub: 'Fiscal brain', x: 380, y: 140, center: true },
  { id: 'researcher', label: 'Researcher', sub: 'Cloud worker', x: 260, y: 260 },
  { id: 'writer', label: 'Writer', sub: 'Polisher', x: 500, y: 260 },
] as const

const EDGES: [string, string][] = [
  ['user', 'guard'],
  ['guard', 'accountant'],
  ['accountant', 'researcher'],
  ['accountant', 'writer'],
  ['researcher', 'writer'],
]

function nodeById(id: string) {
  return NODES.find((n) => n.id === id)!
}

export function ArchitectureMesh() {
  const [hover, setHover] = useState<string | null>(null)

  return (
    <section className="border-b border-cyber-border bg-cyber-surface/30 px-6 py-16 md:py-24">
      <div className="mx-auto max-w-6xl">
        <h2 className="text-center text-2xl font-bold tracking-tight text-slate-100 md:text-3xl">
          Architecture mesh
        </h2>
        <p className="mx-auto mt-3 max-w-2xl text-center text-slate-400">
          Data flows through the Budget Guard into the Accountant — the central brain for forecasts,
          clearance, and circuit-breaker policy — then into the agent mesh.
        </p>

        <div className="mt-12 overflow-x-auto rounded-xl border border-cyber-border bg-cyber-void p-4 md:p-8">
          <svg
            viewBox="0 0 620 320"
            className="mx-auto min-w-[520px] w-full max-w-[620px]"
            role="img"
            aria-label="Architecture: User to Budget Guard to Accountant to Researcher and Writer"
          >
            <defs>
              <linearGradient id="edgeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#22d3ee" stopOpacity="0.25" />
                <stop offset="50%" stopColor="#34d399" stopOpacity="0.6" />
                <stop offset="100%" stopColor="#22d3ee" stopOpacity="0.25" />
              </linearGradient>
              <filter id="glow">
                <feGaussianBlur stdDeviation="2" result="b" />
                <feMerge>
                  <feMergeNode in="b" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            {EDGES.map(([from, to], i) => {
              const a = nodeById(from)
              const b = nodeById(to)
              const hx = (a.x + b.x) / 2
              const hy = (a.y + b.y) / 2 - (from === 'researcher' && to === 'writer' ? 0 : 20)
              const d = `M ${a.x} ${a.y} Q ${hx} ${hy} ${b.x} ${b.y}`
              const active = hover === from || hover === to || hover === null
              return (
                <g key={`${from}-${to}`}>
                  <motion.path
                    d={d}
                    fill="none"
                    stroke="url(#edgeGrad)"
                    strokeWidth={active ? 2 : 1}
                    strokeOpacity={active ? 0.9 : 0.35}
                    strokeDasharray="6 4"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 1.2, delay: 0.08 * i, ease: 'easeOut' }}
                  />
                  <motion.path
                    d={d}
                    fill="none"
                    stroke="#22d3ee"
                    strokeWidth={1.5}
                    strokeDasharray="4 200"
                    strokeOpacity={hover ? 0.45 : 0.15}
                    initial={{ strokeDashoffset: 0 }}
                    animate={{ strokeDashoffset: hover ? -220 : 0 }}
                    transition={{
                      strokeDashoffset: { duration: 2.8, repeat: Infinity, ease: 'linear' },
                    }}
                  />
                </g>
              )
            })}

            {NODES.map((n) => {
              const isCenter = 'center' in n && n.center
              const isHover = hover === n.id
              return (
                <g
                  key={n.id}
                  onMouseEnter={() => setHover(n.id)}
                  onMouseLeave={() => setHover(null)}
                  style={{ cursor: 'pointer' }}
                >
                  <motion.rect
                    x={n.x - (isCenter ? 72 : 58)}
                    y={n.y - 28}
                    width={isCenter ? 144 : 116}
                    height={56}
                    rx={10}
                    fill={isCenter ? '#0f172a' : '#111a24'}
                    stroke={
                      isCenter
                        ? isHover
                          ? '#34d399'
                          : 'rgba(52,211,153,0.65)'
                        : isHover
                          ? '#22d3ee'
                          : '#1e2d3d'
                    }
                    strokeWidth={isCenter ? 2 : 1.5}
                    filter={isCenter ? 'url(#glow)' : undefined}
                    initial={{ opacity: 0, scale: 0.92 }}
                    animate={{
                      opacity: 1,
                      scale: isHover ? 1.03 : 1,
                    }}
                    transition={{ duration: 0.35 }}
                  />
                  <text
                    x={n.x}
                    y={n.y - 4}
                    textAnchor="middle"
                    className="fill-slate-100 text-[11px] font-semibold"
                    style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}
                  >
                    {n.label}
                  </text>
                  <text
                    x={n.x}
                    y={n.y + 12}
                    textAnchor="middle"
                    className="fill-slate-500 text-[9px]"
                    style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}
                  >
                    {n.sub}
                  </text>
                </g>
              )
            })}
          </svg>
        </div>
        <p className="mt-4 text-center text-xs text-slate-500">
          Hover nodes to trace routing. The Accountant agent is the hub of fiscal logic.
        </p>
      </div>
    </section>
  )
}
