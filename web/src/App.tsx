import { HeroSection } from './components/HeroSection'
import { SimulationDashboard } from './components/SimulationDashboard'
import { GovernanceMetrics } from './components/GovernanceMetrics'
import { ArchitectureMesh } from './components/ArchitectureMesh'
import { EvidenceSection } from './components/EvidenceSection'
import { PaperSection } from './components/PaperSection'

export default function App() {
  return (
    <div className="min-h-svh">
      <HeroSection />
      <SimulationDashboard />
      <GovernanceMetrics />
      <ArchitectureMesh />
      <EvidenceSection />
      <PaperSection />
      <footer className="border-t border-cyber-border px-6 py-8 text-center text-xs text-slate-600">
        Budget-Aware AI Squad · Autonomous Cloud Governance · CSCI-750 Cloud Computing
      </footer>
    </div>
  )
}
