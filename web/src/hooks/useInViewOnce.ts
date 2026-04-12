import { useEffect, useRef, useState } from 'react'

export function useInViewOnce(options?: IntersectionObserverInit) {
  const ref = useRef<HTMLElement | null>(null)
  const [inView, setInView] = useState(false)

  useEffect(() => {
    const el = ref.current
    if (!el || inView) return
    const obs = new IntersectionObserver(
      ([e]) => {
        if (e?.isIntersecting) {
          setInView(true)
          obs.disconnect()
        }
      },
      { rootMargin: '0px 0px -12% 0px', threshold: 0.15, ...options }
    )
    obs.observe(el)
    return () => obs.disconnect()
  }, [inView, options])

  return { ref, inView }
}
