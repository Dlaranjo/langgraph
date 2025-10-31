"use client"

import { useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Loader2, Search, Download, CheckCircle2, AlertCircle, XCircle } from "lucide-react"

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
  const [tavilyKey, setTavilyKey] = useState("")
  const [maxIterations, setMaxIterations] = useState(1)
  const [useTavily, setUseTavily] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ResearchResult | null>(null)
  const [error, setError] = useState<string | null>(null)

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
          tavily_api_key: useTavily ? tavilyKey : null,
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
      <div className="container mx-auto py-10 px-4 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
            🔬 Agente Pesquisador IA
          </h1>
          <p className="text-muted-foreground text-lg">
            Pesquisa inteligente com validação de fontes e geração de relatórios
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Search Card */}
            <Card>
              <CardHeader>
                <CardTitle>💭 Faça sua pergunta</CardTitle>
                <CardDescription>
                  Digite uma pergunta e nosso agente irá pesquisar e validar as informações
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="query">Pergunta de Pesquisa</Label>
                  <Textarea
                    id="query"
                    placeholder="Ex: Quais são os principais benefícios e riscos da inteligência artificial generativa?"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    rows={3}
                    className="resize-none"
                  />
                </div>

                <div className="flex gap-3">
                  <Button
                    onClick={handleSearch}
                    disabled={loading}
                    className="flex-1"
                    size="lg"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Pesquisando...
                      </>
                    ) : (
                      <>
                        <Search className="mr-2 h-4 w-4" />
                        Pesquisar
                      </>
                    )}
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setQuery("")
                      setResult(null)
                      setError(null)
                    }}
                    size="lg"
                  >
                    Limpar
                  </Button>
                </div>

                {error && (
                  <div className="p-4 bg-destructive/10 text-destructive rounded-lg border border-destructive/20">
                    <p className="font-semibold">❌ Erro:</p>
                    <p className="text-sm mt-1">{error}</p>
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
                      <div className="prose prose-purple max-w-none prose-headings:text-purple-900 prose-a:text-purple-600 prose-strong:text-purple-800">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
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
                              <p className="text-sm">
                                <strong>URL:</strong>{" "}
                                <a
                                  href={ref.source || ref.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-primary hover:underline"
                                >
                                  {ref.source || ref.url}
                                </a>
                              </p>
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
                  <Label htmlFor="anthropic-key">ANTHROPIC_API_KEY *</Label>
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
                  <Label htmlFor="iterations">Máximo de Iterações</Label>
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

                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="use-tavily"
                    checked={useTavily}
                    onChange={(e) => setUseTavily(e.target.checked)}
                    className="rounded"
                  />
                  <Label htmlFor="use-tavily">Usar Tavily API (busca real)</Label>
                </div>

                {useTavily && (
                  <div className="space-y-2">
                    <Label htmlFor="tavily-key">Tavily API Key</Label>
                    <Input
                      id="tavily-key"
                      type="password"
                      placeholder="tvly-..."
                      value={tavilyKey}
                      onChange={(e) => setTavilyKey(e.target.value)}
                    />
                  </div>
                )}
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
