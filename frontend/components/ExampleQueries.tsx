"use client"

import { Lightbulb, Copy, Sparkles } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

interface ExampleQuery {
  id: string
  query: string
  category: string
  description: string
  iterations: number
}

const EXAMPLE_QUERIES: ExampleQuery[] = [
  {
    id: "tech-comparison",
    query: "Compare as vantagens e desvantagens de GraphQL vs REST API para aplicações web modernas",
    category: "Tecnologia",
    description: "Análise comparativa de tecnologias",
    iterations: 2
  },
  {
    id: "ai-risks",
    query: "Quais são os principais benefícios e riscos da inteligência artificial generativa?",
    category: "IA",
    description: "Pesquisa balanceada sobre IA",
    iterations: 2
  },
  {
    id: "quantum-computing",
    query: "Explique computação quântica de forma simples e suas aplicações práticas atuais",
    category: "Ciência",
    description: "Explicação simplificada de conceito complexo",
    iterations: 1
  },
  {
    id: "climate-solutions",
    query: "Quais são as soluções mais promissoras para combater as mudanças climáticas segundo a ciência atual?",
    category: "Meio Ambiente",
    description: "Pesquisa baseada em evidências científicas",
    iterations: 2
  },
  {
    id: "microservices",
    query: "Quando devo usar arquitetura de microserviços vs arquitetura monolítica?",
    category: "Engenharia",
    description: "Decisão arquitetural com prós e contras",
    iterations: 2
  },
  {
    id: "blockchain",
    query: "Quais são os casos de uso reais e práticos de blockchain além de criptomoedas?",
    category: "Tecnologia",
    description: "Aplicações práticas de tecnologia",
    iterations: 1
  }
]

interface ExampleQueriesProps {
  onSelectQuery: (query: string, iterations: number) => void
}

export function ExampleQueries({ onSelectQuery }: ExampleQueriesProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Lightbulb className="h-5 w-5 text-yellow-500" />
          Exemplos de Perguntas
        </CardTitle>
        <CardDescription>
          Clique em um exemplo para começar rapidamente
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {EXAMPLE_QUERIES.map((example) => (
          <div
            key={example.id}
            className="group relative border rounded-lg p-3 hover:border-purple-300 hover:bg-purple-50/50 transition-all cursor-pointer"
            onClick={() => onSelectQuery(example.query, example.iterations)}
          >
            <div className="flex items-start justify-between gap-2 mb-2">
              <Badge variant="outline" className="text-xs">
                {example.category}
              </Badge>
              <div className="flex items-center gap-1 text-xs text-muted-foreground">
                <Sparkles className="h-3 w-3" />
                {example.iterations} {example.iterations === 1 ? 'iteração' : 'iterações'}
              </div>
            </div>

            <p className="text-sm font-medium text-gray-900 mb-1 group-hover:text-purple-700 transition-colors">
              {example.query}
            </p>

            <p className="text-xs text-muted-foreground">
              {example.description}
            </p>

            <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
              <Copy className="h-4 w-4 text-purple-600" />
            </div>
          </div>
        ))}

        <div className="mt-4 p-3 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg border border-purple-100">
          <p className="text-xs text-purple-900 font-medium flex items-center gap-2">
            <Lightbulb className="h-4 w-4" />
            Dica: Perguntas específicas e bem formuladas geram melhores resultados!
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
