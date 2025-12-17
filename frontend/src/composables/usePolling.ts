/**
 * Composable for polling data at regular intervals.
 */

import { ref, onUnmounted } from 'vue'

export function usePolling(callback: () => Promise<void>, interval: number = 3000) {
  const isPolling = ref(false)
  let timerId: number | null = null

  function start() {
    if (isPolling.value) return

    isPolling.value = true
    poll()
  }

  function stop() {
    isPolling.value = false
    if (timerId !== null) {
      clearTimeout(timerId)
      timerId = null
    }
  }

  async function poll() {
    if (!isPolling.value) return

    try {
      await callback()
    } catch (e) {
      console.error('Polling error:', e)
    }

    if (isPolling.value) {
      timerId = window.setTimeout(poll, interval)
    }
  }

  onUnmounted(() => {
    stop()
  })

  return {
    isPolling,
    start,
    stop
  }
}

