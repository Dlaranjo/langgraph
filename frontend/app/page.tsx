"use client"

import { useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { TextareaWithButton } from "@/components/ui/textarea-with-button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Loader2, Search, Download, CheckCircle2, AlertCircle, XCircle, RotateCcw } from "lucide-react"
import { HelpPanel } from "@/components/HelpPanel"
import { QuickExamples } from "@/components/QuickExamples"
import { InfoTooltip } from "@/components/InfoTooltip"
import { OnboardingTour, useOnboardingTour } from "@/components/OnboardingTour"

interface ResearchResult {
  query: string
  timestamp: string
  report: string
  confidence: number
  search_results_count: number
  validations_count: number
  iterations: number
  conflicts_detected: boolean
  references: Array<{
    title?: string
    source?: string
    url?: string
    relevance_score?: number
  }>
  full_state?: {
    messages?: string[]
    validations?: Array<{
      claim: string
      is_validated: boolean
      confidence: number
      reasoning: string
    }>
    search_queries?: string[]
  }
}

export default function Home() {
  const [query, setQuery] = useState("")
  const [anthropicKey, setAnthropicKey] = useState("")
  const [maxIterations, setMaxIterations] = useState(1)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ResearchResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const { resetOnboarding } = useOnboardingTour()

  const handleSelectExample = (exampleQuery: string, iterations: number) => {
    setQuery(exampleQuery)
    setMaxIterations(iterations)
  }

  const handleSearch = async () => {
    if (!query.trim() || !anthropicKey.trim()) {
      setError("Por favor, preencha a pergunta e a API key")
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch("http://localhost:8000/research", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query,
          max_iterations: maxIterations,
          anthropic_api_key: anthropicKey,
        }),
      })

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.statusText}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido")
    } finally {
      setLoading(false)
    }
  }

  const downloadReport = () => {
    if (!result) return
    const blob = new Blob([result.report], { type: "text/markdown" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `relatorio_${new Date().toISOString().slice(0, 10)}.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <OnboardingTour />
      <div className="container mx-auto py-10 px-4 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              🔬 Agente Pesquisador IA
            </h1>
          </div>
          <p className="text-muted-foreground text-lg mb-4">
            Pesquisa inteligente com validação de fontes e geração de relatórios
          </p>
          <div className="flex items-center justify-center gap-2">
            <HelpPanel />
            <Button
              variant="outline"
              size="sm"
              onClick={resetOnboarding}
              className="gap-2"
            >
              <RotateCcw className="h-4 w-4" />
              Ver Tour Novamente
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Search Card */}
            <Card>
              <CardHeader>
                <CardTitle>💡 Pesquise com inteligência</CardTitle>
                <CardDescription>
                  IA que busca, valida e sintetiza informações de múltiplas fontes automaticamente
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <TextareaWithButton
                    id="query"
                    placeholder="Digite sua pergunta aqui... (Enter para enviar, Shift+Enter para nova linha)"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onSubmit={handleSearch}
                    loading={loading}
                    submitDisabled={!query.trim() || !anthropicKey.trim()}
                    rows={4}
                  />

                  {/* Quick examples (pills) - sempre visível quando não há resultado/loading */}
                  {!result && !loading && (
                    <QuickExamples onSelect={handleSelectExample} />
                  )}
                </div>

                {error && (
                  <div className="p-4 bg-destructive/10 text-destructive rounded-lg border border-destructive/20">
                    <p className="font-semibold flex items-center gap-2">
                      <XCircle className="h-4 w-4" />
                      Erro
                    </p>
                    <p className="text-sm mt-1">{error}</p>
                  </div>
                )}

                {loading && (
                  <div className="p-4 bg-purple-50 text-purple-900 rounded-lg border border-purple-200">
                    <p className="font-semibold flex items-center gap-2">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Pesquisando...
                    </p>
                    <p className="text-sm mt-1">
                      O agente está coletando e validando informações. Isso pode levar alguns instantes.
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Results */}
            {result && (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>📋 Resultados da Pesquisa</CardTitle>
                    <Button variant="outline" size="sm" onClick={downloadReport}>
                      <Download className="mr-2 h-4 w-4" />
                      Baixar Relatório
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <Tabs defaultValue="report" className="w-full">
                    <TabsList className="grid w-full grid-cols-5">
                      <TabsTrigger value="report">📄 Relatório</TabsTrigger>
                      <TabsTrigger value="references">📚 Fontes</TabsTrigger>
                      <TabsTrigger value="analysis">📊 Análise</TabsTrigger>
                      <TabsTrigger value="logs">📋 Logs</TabsTrigger>
                      <TabsTrigger value="details">🔍 Detalhes</TabsTrigger>
                    </TabsList>

                    <TabsContent value="report" className="space-y-4">
                      <div className="prose prose-slate max-w-none">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            h1: ({node, ...props}) => <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-6 mb-3 pb-2 border-b border-gray-200" {...props} />,
                            h2: ({node, ...props}) => <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200 mt-5 mb-2.5" {...props} />,
                            h3: ({node, ...props}) => <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mt-4 mb-2" {...props} />,
                            h4: ({node, ...props}) => <h4 className="text-base font-semibold text-gray-700 dark:text-gray-300 mt-3 mb-1.5" {...props} />,
                            p: ({node, ...props}) => <p className="text-[15px] text-gray-700 dark:text-gray-300 leading-7 mb-3" {...props} />,
                            ul: ({node, ...props}) => <ul className="list-disc ml-6 mb-3 space-y-1" {...props} />,
                            ol: ({node, ...props}) => <ol className="list-decimal ml-6 mb-3 space-y-1" {...props} />,
                            li: ({node, ...props}) => <li className="text-[15px] text-gray-700 dark:text-gray-300 leading-7" {...props} />,
                            strong: ({node, ...props}) => <strong className="font-semibold text-gray-900 dark:text-gray-100" {...props} />,
                            em: ({node, ...props}) => <em className="italic text-gray-700 dark:text-gray-300" {...props} />,
                            a: ({node, ...props}) => <a className="text-purple-600 dark:text-purple-400 underline hover:text-purple-800 dark:hover:text-purple-300 transition-colors break-all" {...props} target="_blank" rel="noopener noreferrer" />,
                            code: ({node, inline, ...props}: any) =>
                              inline
                                ? <code className="bg-gray-100 dark:bg-gray-800 text-purple-600 dark:text-purple-400 px-1.5 py-0.5 rounded text-[13px] font-mono" {...props} />
                                : <code className="block bg-gray-900 dark:bg-gray-950 text-gray-100 p-3 rounded-md overflow-x-auto font-mono text-[13px] leading-6" {...props} />,
                            pre: ({node, ...props}) => <pre className="bg-gray-900 dark:bg-gray-950 rounded-md overflow-hidden mb-3 shadow-sm" {...props} />,
                            blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-purple-400 dark:border-purple-600 pl-4 py-1 italic text-gray-600 dark:text-gray-400 my-3 bg-purple-50/50 dark:bg-purple-950/20" {...props} />,
                            hr: ({node, ...props}) => <hr className="border-gray-200 dark:border-gray-700 my-6" {...props} />,
                            table: ({node, ...props}) => <div className="overflow-x-auto mb-4 rounded-md border border-gray-200 dark:border-gray-700"><table className="min-w-full border-collapse" {...props} /></div>,
                            thead: ({node, ...props}) => <thead className="bg-gray-50 dark:bg-gray-800" {...props} />,
                            th: ({node, ...props}) => <th className="border-b border-gray-200 dark:border-gray-700 px-4 py-2 text-left text-sm font-semibold text-gray-900 dark:text-gray-100" {...props} />,
                            td: ({node, ...props}) => <td className="border-b border-gray-200 dark:border-gray-700 px-4 py-2 text-sm text-gray-700 dark:text-gray-300" {...props} />,
                          }}
                        >
                          {result.report}
                        </ReactMarkdown>
                      </div>
                    </TabsContent>

                    <TabsContent value="references" className="space-y-4">
                      {result.references && result.references.length > 0 ? (
                        result.references.map((ref, idx) => (
                          <Card key={idx}>
                            <CardHeader>
                              <CardTitle className="text-base">
                                📌 Fonte {idx + 1}: {ref.title || "Sem título"}
                              </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-2">
                              <div className="text-sm">
                                <strong>URL:</strong>{" "}
                                <a
                                  href={ref.source || ref.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-primary hover:underline break-all"
                                >
                                  {ref.source || ref.url}
                                </a>
                              </div>
                              {ref.relevance_score !== undefined && (
                                <div className="space-y-1">
                                  <p className="text-sm font-semibold">
                                    Relevância: {(ref.relevance_score * 100).toFixed(0)}%
                                  </p>
                                  <div className="w-full bg-secondary rounded-full h-2">
                                    <div
                                      className="bg-gradient-to-r from-purple-600 to-pink-600 h-2 rounded-full transition-all"
                                      style={{ width: `${ref.relevance_score * 100}%` }}
                                    />
                                  </div>
                                </div>
                              )}
                            </CardContent>
                          </Card>
                        ))
                      ) : (
                        <p className="text-muted-foreground text-center py-8">
                          Nenhuma referência disponível
                        </p>
                      )}
                    </TabsContent>

                    <TabsContent value="analysis" className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <Card>
                          <CardHeader>
                            <CardTitle className="text-base">Nível de Confiança</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                              {(result.confidence * 100).toFixed(0)}%
                            </div>
                            <div className="w-full bg-secondary rounded-full h-3 mt-3">
                              <div
                                className="bg-gradient-to-r from-purple-600 to-pink-600 h-3 rounded-full transition-all"
                                style={{ width: `${result.confidence * 100}%` }}
                              />
                            </div>
                          </CardContent>
                        </Card>

                        <Card>
                          <CardHeader>
                            <CardTitle className="text-base">Métricas</CardTitle>
                          </CardHeader>
                          <CardContent className="space-y-2">
                            <div className="flex justify-between">
                              <span className="text-sm">Fontes:</span>
                              <Badge>{result.search_results_count}</Badge>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-sm">Validações:</span>
                              <Badge>{result.validations_count}</Badge>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-sm">Iterações:</span>
                              <Badge>{result.iterations}</Badge>
                            </div>
                          </CardContent>
                        </Card>
                      </div>
                    </TabsContent>

                    <TabsContent value="logs" className="space-y-2">
                      {result.full_state?.messages && result.full_state.messages.length > 0 ? (
                        <div className="space-y-1 max-h-96 overflow-y-auto">
                          {result.full_state.messages.map((msg, idx) => (
                            <div
                              key={idx}
                              className="p-2 text-sm font-mono bg-muted rounded"
                            >
                              {msg}
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-muted-foreground text-center py-8">
                          Nenhum log disponível
                        </p>
                      )}
                    </TabsContent>

                    <TabsContent value="details" className="space-y-4">
                      {result.full_state?.validations && (
                        <Card>
                          <CardHeader>
                            <CardTitle className="text-base">✅ Validações</CardTitle>
                          </CardHeader>
                          <CardContent className="space-y-3">
                            {result.full_state.validations.map((val, idx) => (
                              <div key={idx} className="border-l-4 border-primary pl-4 space-y-1">
                                <p className="font-semibold text-sm">{val.claim}</p>
                                <div className="flex items-center gap-2">
                                  {val.is_validated ? (
                                    <CheckCircle2 className="h-4 w-4 text-green-600" />
                                  ) : (
                                    <XCircle className="h-4 w-4 text-red-600" />
                                  )}
                                  <span className="text-sm text-muted-foreground">
                                    Confiança: {(val.confidence * 100).toFixed(0)}%
                                  </span>
                                </div>
                                <p className="text-sm text-muted-foreground">{val.reasoning}</p>
                              </div>
                            ))}
                          </CardContent>
                        </Card>
                      )}

                      {result.full_state?.search_queries && (
                        <Card>
                          <CardHeader>
                            <CardTitle className="text-base">🔍 Queries Geradas</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <ul className="list-disc list-inside space-y-1">
                              {result.full_state.search_queries.map((q, idx) => (
                                <li key={idx} className="text-sm">{q}</li>
                              ))}
                            </ul>
                          </CardContent>
                        </Card>
                      )}
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Configuration */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base">⚙️ Configurações</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Label htmlFor="anthropic-key">ANTHROPIC_API_KEY *</Label>
                    <InfoTooltip
                      content={
                        <div>
                          <p className="font-semibold mb-1">API Key da Anthropic</p>
                          <p className="mb-2">Necessária para usar o modelo Claude.</p>
                          <p className="text-xs">
                            Obtenha em:{" "}
                            <a
                              href="https://console.anthropic.com/"
                              target="_blank"
                              rel="noopener noreferrer"
                              className="underline"
                            >
                              console.anthropic.com
                            </a>
                          </p>
                        </div>
                      }
                    />
                  </div>
                  <Input
                    id="anthropic-key"
                    type="password"
                    placeholder="sk-ant-..."
                    value={anthropicKey}
                    onChange={(e) => setAnthropicKey(e.target.value)}
                  />
                </div>

                <Separator />

                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Label htmlFor="iterations">Máximo de Iterações</Label>
                    <InfoTooltip
                      content={
                        <div>
                          <p className="font-semibold mb-1">Ciclos de Pesquisa</p>
                          <ul className="space-y-1 text-xs">
                            <li><strong>1 iteração:</strong> Rápida, ideal para perguntas simples</li>
                            <li><strong>2 iterações:</strong> Balanceada, boa para análises comparativas</li>
                            <li><strong>3 iterações:</strong> Completa, máxima confiabilidade</li>
                          </ul>
                          <p className="mt-2 text-xs text-yellow-200">⚠️ Mais iterações = mais tempo e custo</p>
                        </div>
                      }
                    />
                  </div>
                  <Input
                    id="iterations"
                    type="number"
                    min="1"
                    max="3"
                    value={maxIterations}
                    onChange={(e) => setMaxIterations(parseInt(e.target.value))}
                  />
                  <p className="text-xs text-muted-foreground">
                    Número de ciclos de busca e validação (1-3)
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Status */}
            {result && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">📊 Status</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Confiança:</span>
                    <Badge variant={result.confidence > 0.75 ? "default" : "secondary"}>
                      {(result.confidence * 100).toFixed(0)}%
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Fontes:</span>
                    <Badge variant="outline">{result.search_results_count}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Validações:</span>
                    <Badge variant="outline">{result.validations_count}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Iterações:</span>
                    <Badge variant="outline">{result.iterations}</Badge>
                  </div>
                  <Separator />
                  <div className="flex items-center gap-2">
                    {result.conflicts_detected ? (
                      <>
                        <AlertCircle className="h-4 w-4 text-yellow-600" />
                        <span className="text-sm">Conflitos detectados</span>
                      </>
                    ) : (
                      <>
                        <CheckCircle2 className="h-4 w-4 text-green-600" />
                        <span className="text-sm">Sem conflitos</span>
                      </>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-sm text-muted-foreground">
          <p>🤖 Powered by LangGraph + Claude | 💻 Next.js + shadcn/ui | 🚀 FastAPI</p>
        </div>
      </div>
    </div>
  )
}
