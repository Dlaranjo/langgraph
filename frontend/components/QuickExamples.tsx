"use client"

import { Sparkles } from "lucide-react"
import { Badge } from "@/components/ui/badge"

interface QuickExample {
  label: string
  query: string
  iterations: number
}

const QUICK_EXAMPLES: QuickExample[] = [
  { label: "IA Generativa", query: "Quais são os principais benefícios e riscos da IA generativa?", iterations: 2 },
  { label: "GraphQL vs REST", query: "Compare as vantagens e desvantagens de GraphQL vs REST API", iterations: 2 },
  { label: "Computação Quântica", query: "Explique computação quântica de forma simples", iterations: 1 },
  { label: "Microserviços", query: "Microserviços vs arquitetura monolítica: quando usar?", iterations: 2 },
]

interface QuickExamplesProps {
  onSelect: (query: string, iterations: number) => void
}

export function QuickExamples({ onSelect }: QuickExamplesProps) {
  return (
    <div className="space-y-2">
      <p className="text-xs text-muted-foreground flex items-center gap-1.5">
        <Sparkles className="h-3 w-3" />
        Experimente estas sugestões:
      </p>
      <div className="flex flex-wrap gap-2">
        {QUICK_EXAMPLES.map((example) => (
          <button
            key={example.label}
            onClick={() => onSelect(example.query, example.iterations)}
            className="group"
          >
            <Badge
              variant="outline"
              className="cursor-pointer hover:bg-purple-50 hover:border-purple-300 hover:text-purple-700 transition-all"
            >
              <span>{example.label}</span>
              <span className="ml-1 text-xs opacity-60">{example.iterations}x</span>
            </Badge>
          </button>
        ))}
      </div>
    </div>
  )
}
