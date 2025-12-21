/**
 * Composable for Dashboard data fetching
 * Aggregates data from existing APIs for the home page dashboard
 */

import { ref, onMounted } from 'vue'
import { getMediaApiStatus } from '@/api/media'
import { getReports } from '@/api/report'
import { getCrawlerStatus } from '@/api/mediaCrawler'
import type { DashboardStats, RecentReport } from '@/types/dashboard'
import type { ReportListItem } from '@/types/report'

export function useDashboard() {
  const stats = ref<DashboardStats>({
    totalRecords: 0,
    totalReports: 0,
    activePlatforms: 0,
    crawlerStatus: 'idle',
  })

  const recentReports = ref<RecentReport[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  async function fetchStats() {
    loading.value = true
    error.value = null

    try {
      // Fetch in parallel
      const [apiStatus, reportsResponse, crawlerStatusResponse] = await Promise.allSettled([
        getMediaApiStatus(),
        getReports(5, 0),
        getCrawlerStatus(),
      ])

      // Process API status
      if (apiStatus.status === 'fulfilled') {
        stats.value.activePlatforms = apiStatus.value.platforms?.length || 0
      }

      // Process reports
      if (reportsResponse.status === 'fulfilled') {
        stats.value.totalReports = reportsResponse.value.total || 0
        recentReports.value = reportsResponse.value.items.map((report: ReportListItem) => ({
          id: report.id,
          title: report.title,
          platform: report.platform,
          createdAt: report.created_at,
        }))
      }

      // Process crawler status
      if (crawlerStatusResponse.status === 'fulfilled') {
        stats.value.crawlerStatus = crawlerStatusResponse.value.status || 'idle'
      }

      // Estimate total records from reports (simplified approach)
      // In a real scenario, we'd have a dedicated stats endpoint
      if (reportsResponse.status === 'fulfilled') {
        const reports = reportsResponse.value.items
        stats.value.totalRecords = reports.reduce(
          (sum: number, r: ReportListItem) => sum + (r.record_count || 0),
          0
        )
      }
    } catch (e: unknown) {
      console.error('Failed to fetch dashboard stats:', e)
      error.value = e instanceof Error ? e.message : '加载仪表盘数据失败'
    } finally {
      loading.value = false
    }
  }

  async function refresh() {
    await fetchStats()
  }

  onMounted(() => {
    fetchStats()
  })

  return {
    stats,
    recentReports,
    loading,
    error,
    refresh,
  }
}

