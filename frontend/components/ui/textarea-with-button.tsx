"use client"

import * as React from "react"
import { Loader2, ArrowUp } from "lucide-react"
import { cn } from "@/lib/utils"

export interface TextareaWithButtonProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  onSubmit?: () => void
  loading?: boolean
  submitDisabled?: boolean
}

const TextareaWithButton = React.forwardRef<
  HTMLTextAreaElement,
  TextareaWithButtonProps
>(({ className, onSubmit, loading = false, submitDisabled = false, ...props }, ref) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Enter sem Shift envia
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      if (!submitDisabled && !loading && onSubmit) {
        onSubmit()
      }
    }
    // Chama o onKeyDown original se existir
    if (props.onKeyDown) {
      props.onKeyDown(e)
    }
  }

  return (
    <div className="relative">
      <textarea
        className={cn(
          "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 pr-12 resize-none",
          className
        )}
        ref={ref}
        onKeyDown={handleKeyDown}
        {...props}
      />

      {/* Botão de envio integrado */}
      <button
        type="button"
        onClick={onSubmit}
        disabled={submitDisabled || loading}
        className={cn(
          "absolute bottom-2 right-2 h-8 w-8 rounded-lg flex items-center justify-center transition-all",
          "focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
          submitDisabled || loading
            ? "bg-muted text-muted-foreground cursor-not-allowed"
            : "bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-700 hover:to-pink-700 shadow-md hover:shadow-lg"
        )}
        aria-label={loading ? "Pesquisando..." : "Enviar pesquisa"}
      >
        {loading ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : (
          <ArrowUp className="h-4 w-4" />
        )}
      </button>

      {/* Indicador de "Shift+Enter para nova linha" */}
      {!loading && !submitDisabled && (
        <div className="absolute bottom-2 left-3 text-xs text-muted-foreground pointer-events-none opacity-0 hover:opacity-100 transition-opacity">
          <kbd className="px-1.5 py-0.5 text-xs font-semibold bg-muted rounded">Enter</kbd> para enviar • <kbd className="px-1.5 py-0.5 text-xs font-semibold bg-muted rounded">Shift</kbd>+<kbd className="px-1.5 py-0.5 text-xs font-semibold bg-muted rounded">Enter</kbd> para nova linha
        </div>
      )}
    </div>
  )
})
TextareaWithButton.displayName = "TextareaWithButton"

export { TextareaWithButton }
