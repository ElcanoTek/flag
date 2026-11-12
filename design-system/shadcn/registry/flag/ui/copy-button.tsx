"use client"

import * as React from "react"
import { CheckIcon, CopyIcon } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/registry/flag/ui/button"

// Clipboard action button built on Flag's Button: swaps CopyIcon -> CheckIcon
// (in --color-success) for `copiedDurationMs`, keeps an accessible label, and
// announces completion politely. Tier A: .btn.btn-copy[data-copied].
function CopyButton({
  value,
  label = "Copy",
  copiedLabel = "Copied",
  copiedDurationMs = 1800,
  variant = "ghost",
  size = "icon-sm",
  type = "button",
  className,
  children,
  onClick,
  onCopySuccess,
  "aria-label": ariaLabel,
  ...props
}: Omit<React.ComponentProps<typeof Button>, "asChild"> & {
  value: string
  label?: string
  copiedLabel?: string
  copiedDurationMs?: number
  onCopySuccess?: (value: string) => void
}) {
  const [copied, setCopied] = React.useState(false)
  const timeoutRef = React.useRef<ReturnType<typeof setTimeout> | null>(null)

  React.useEffect(() => {
    return () => {
      if (timeoutRef.current !== null) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [])

  const resolvedAriaLabel =
    ariaLabel ?? (children ? undefined : copied ? copiedLabel : label)

  return (
    <Button
      type={type}
      variant={variant}
      size={size}
      aria-label={resolvedAriaLabel}
      className={cn(className)}
      onClick={(event) => {
        onClick?.(event)
        if (event.defaultPrevented || !navigator.clipboard?.writeText) return
        void navigator.clipboard.writeText(value).then(
          () => {
            setCopied(true)
            onCopySuccess?.(value)
            if (timeoutRef.current !== null) {
              clearTimeout(timeoutRef.current)
            }
            timeoutRef.current = setTimeout(() => {
              setCopied(false)
              timeoutRef.current = null
            }, copiedDurationMs)
          },
          () => {
            /* clipboard write may fail in non-secure contexts */
          }
        )
      }}
      {...props}
      data-slot="copy-button"
      data-copied={copied ? "true" : undefined}
    >
      {copied ? (
        <CheckIcon aria-hidden="true" className="text-success" />
      ) : (
        <CopyIcon aria-hidden="true" />
      )}
      {children}
      <span className="sr-only" aria-live="polite">
        {copied ? copiedLabel : ""}
      </span>
    </Button>
  )
}

export { CopyButton }
