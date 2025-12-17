<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import * as echarts from 'echarts'
import type { GraphNode, GraphEdge } from '@/types/graph'

const props = defineProps<{
  nodes: GraphNode[]
  edges: GraphEdge[]
}>()

const emit = defineEmits<{
  nodeClick: [node: GraphNode]
}>()

const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

// Node colors by type
const nodeColors: Record<string, string> = {
  Channel: '#f59e0b',
  Article: '#6366f1',
  Tag: '#10b981'
}

// Node labels translation
const nodeLabels: Record<string, string> = {
  Channel: '频道',
  Article: '文章',
  Tag: '标签'
}

// Node sizes by type
const nodeSizes: Record<string, number> = {
  Channel: 35,
  Article: 25,
  Tag: 18
}

const chartData = computed(() => {
  const categories = [
    { name: nodeLabels.Channel },
    { name: nodeLabels.Article },
    { name: nodeLabels.Tag }
  ]

  // Map original type to category index
  const typeToIndex = {
    Channel: 0,
    Article: 1,
    Tag: 2
  }

  const data = props.nodes.map((node) => ({
    id: node.id,
    name: node.label,
    symbolSize: nodeSizes[node.type] || 20,
    category: typeToIndex[node.type as keyof typeof typeToIndex] ?? -1,
    itemStyle: {
      color: nodeColors[node.type] || '#6366f1'
    },
    properties: node.properties
  }))

  const links = props.edges.map((edge) => ({
    source: edge.source,
    target: edge.target,
    lineStyle: {
      color: edge.type === 'CONTAINS' ? '#f59e0b' : '#10b981',
      opacity: 0.4,
      width: edge.type === 'CONTAINS' ? 2 : 1
    }
  }))

  return { data, links, categories }
})

function initChart() {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value, 'dark')

  updateChart()

  chart.on('click', 'series', (params: any) => {
    if (params.dataType === 'node') {
      const node = props.nodes.find((n) => n.id === params.data.id)
      if (node) {
        emit('nodeClick', node)
      }
    }
  })

  window.addEventListener('resize', handleResize)
}

function updateChart() {
  if (!chart) return

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: '#1e1e2e',
      borderColor: '#3d3d5c',
      textStyle: {
        color: '#e0e0e0'
      },
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          return `<strong>${params.name}</strong><br/>类型: ${chartData.value.categories[params.data.category]?.name || '未知'}`
        }
        return ''
      }
    },
    legend: {
      data: chartData.value.categories.map((c) => c.name),
      orient: 'horizontal',
      left: 'center',
      top: 10,
      textStyle: {
        color: '#a0a0b0'
      },
      itemStyle: {
        borderWidth: 0
      }
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        data: chartData.value.data,
        links: chartData.value.links,
        categories: chartData.value.categories.map((c, i) => ({
          name: c.name,
          itemStyle: {
            color: Object.values(nodeColors)[i]
          }
        })),
        roam: true,
        draggable: true,
        label: {
          show: true,
          position: 'right',
          fontSize: 10,
          color: '#a0a0b0',
          formatter: (params: any) => {
            const name = params.name || ''
            return name.length > 15 ? name.slice(0, 15) + '...' : name
          }
        },
        emphasis: {
          focus: 'adjacency',
          label: {
            show: true,
            fontSize: 12,
            fontWeight: 'bold'
          },
          lineStyle: {
            width: 3
          }
        },
        force: {
          repulsion: 150,
          edgeLength: [50, 150],
          gravity: 0.1
        },
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut'
      }
    ]
  }

  chart.setOption(option, true)
}

function handleResize() {
  chart?.resize()
}

watch(
  () => [props.nodes, props.edges],
  () => {
    updateChart()
  },
  { deep: true }
)

onMounted(() => {
  initChart()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<template>
  <div ref="chartRef" class="graph-canvas"></div>
</template>

<style scoped>
.graph-canvas {
  width: 100%;
  height: 100%;
  min-height: 500px;
}
</style>

