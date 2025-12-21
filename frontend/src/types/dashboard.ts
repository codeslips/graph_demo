/**
 * TypeScript types for Dashboard functionality
 */

export interface DashboardStats {
  totalRecords: number
  totalReports: number
  activePlatforms: number
  crawlerStatus: 'running' | 'idle'
}

export interface RecentReport {
  id: string
  title: string
  platform: string
  createdAt: string
}

export interface DashboardData {
  stats: DashboardStats
  recentReports: RecentReport[]
  loading: boolean
  error: string | null
}

export interface WorkflowStep {
  id: number
  icon: string
  title: string
  description: string
  route: string
}

export interface QuickAction {
  id: string
  icon: string
  label: string
  route: string
  color: string
}

export interface FeatureCard {
  id: string
  icon: string
  title: string
  description: string
  route: string
  color: string
}

