"use client"

import { HelpCircle, BookOpen, Zap, Brain, Shield } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export function HelpPanel() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" className="gap-2">
          <HelpCircle className="h-4 w-4" />
          Ajuda
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-2xl">
            <BookOpen className="h-6 w-6 text-purple-600" />
            Central de Ajuda
          </DialogTitle>
          <DialogDescription>
            Tudo que você precisa saber para usar o Agente Pesquisador IA
          </DialogDescription>
        </DialogHeader>

        <Tabs defaultValue="faq" className="mt-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="faq">FAQ</TabsTrigger>
            <TabsTrigger value="glossary">Glossário</TabsTrigger>
            <TabsTrigger value="tips">Dicas</TabsTrigger>
          </TabsList>

          <TabsContent value="faq" className="space-y-4 mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Como funciona o agente?</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <p>O Agente Pesquisador IA segue 4 etapas principais:</p>
                <ol className="list-decimal list-inside space-y-1 ml-2">
                  <li><strong>Planejamento:</strong> Gera queries de busca específicas baseadas na sua pergunta</li>
                  <li><strong>Busca:</strong> Coleta informações de múltiplas fontes</li>
                  <li><strong>Validação:</strong> Cruza as informações encontradas para verificar consistência</li>
                  <li><strong>Síntese:</strong> Gera um relatório estruturado com referências</li>
                </ol>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Preciso de API keys?</CardTitle>
              </CardHeader>
              <CardContent className="text-sm space-y-2">
                <p><strong>ANTHROPIC_API_KEY (obrigatória):</strong></p>
                <p className="ml-2">Necessária para o modelo de IA (Claude). Obtenha em: <a href="https://console.anthropic.com/" target="_blank" rel="noopener noreferrer" className="text-purple-600 underline">console.anthropic.com</a></p>

                <p className="mt-3"><strong>TAVILY_API_KEY (opcional):</strong></p>
                <p className="ml-2">Para buscas web reais. Sem ela, o agente simula resultados. Obtenha em: <a href="https://tavily.com/" target="_blank" rel="noopener noreferrer" className="text-purple-600 underline">tavily.com</a> (1.000 créditos grátis/mês)</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">O que são iterações?</CardTitle>
              </CardHeader>
              <CardContent className="text-sm">
                <p>Iterações são ciclos de busca e validação. Mais iterações significam:</p>
                <ul className="list-disc list-inside space-y-1 ml-2 mt-2">
                  <li><strong>1 iteração:</strong> Busca rápida, ideal para perguntas simples</li>
                  <li><strong>2 iterações:</strong> Busca aprofundada, valida com mais fontes</li>
                  <li><strong>3 iterações:</strong> Pesquisa exaustiva, máxima confiabilidade</li>
                </ul>
                <p className="mt-2 text-muted-foreground">⚠️ Mais iterações = mais tempo e custo de API</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Como interpretar a confiança?</CardTitle>
              </CardHeader>
              <CardContent className="text-sm">
                <p>O nível de confiança indica a qualidade das informações:</p>
                <ul className="list-disc list-inside space-y-1 ml-2 mt-2">
                  <li><strong>75-100%:</strong> Alta confiança - informações bem validadas</li>
                  <li><strong>50-75%:</strong> Média confiança - algumas inconsistências</li>
                  <li><strong>0-50%:</strong> Baixa confiança - informações conflitantes ou poucas fontes</li>
                </ul>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="glossary" className="space-y-3 mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <Brain className="h-5 w-5 text-purple-600" />
                  Iteração
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm">
                Ciclo completo de busca, validação e análise de informações. Cada iteração pode gerar novas queries baseadas nos resultados anteriores.
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <Shield className="h-5 w-5 text-purple-600" />
                  Validação
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm">
                Processo de cruzamento de informações de múltiplas fontes para verificar consistência, detectar contradições e calcular confiabilidade.
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <Zap className="h-5 w-5 text-purple-600" />
                  Query de Busca
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm">
                Pergunta específica gerada pelo agente para buscar informações relevantes. O agente cria múltiplas queries a partir da sua pergunta original.
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-purple-600" />
                  Referências
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm">
                Fontes de informação consultadas durante a pesquisa, com scores de relevância que indicam o quanto cada fonte contribuiu para o relatório final.
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <HelpCircle className="h-5 w-5 text-purple-600" />
                  Conflito
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm">
                Informações contraditórias encontradas em diferentes fontes. O agente detecta e relata conflitos, permitindo que você analise discrepâncias.
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="tips" className="space-y-4 mt-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">✅ Faça perguntas específicas</CardTitle>
              </CardHeader>
              <CardContent className="text-sm space-y-2">
                <p><strong className="text-green-600">Bom:</strong> "Compare vantagens e desvantagens de GraphQL vs REST API para aplicações web modernas"</p>
                <p><strong className="text-red-600">Ruim:</strong> "O que é API?"</p>
                <p className="text-muted-foreground mt-2">Perguntas específicas geram resultados mais úteis e confiáveis.</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">📚 Use iterações inteligentemente</CardTitle>
              </CardHeader>
              <CardContent className="text-sm space-y-2">
                <ul className="list-disc list-inside space-y-1">
                  <li>Para <strong>fatos simples</strong>: 1 iteração é suficiente</li>
                  <li>Para <strong>análises comparativas</strong>: use 2 iterações</li>
                  <li>Para <strong>pesquisas acadêmicas</strong>: considere 3 iterações</li>
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">🔍 Explore todas as tabs</CardTitle>
              </CardHeader>
              <CardContent className="text-sm">
                <p>Cada tab oferece insights diferentes:</p>
                <ul className="list-disc list-inside space-y-1 mt-2">
                  <li><strong>Relatório:</strong> Resultado principal com análise completa</li>
                  <li><strong>Fontes:</strong> Verifique as referências e relevância</li>
                  <li><strong>Análise:</strong> Métricas de qualidade da pesquisa</li>
                  <li><strong>Logs:</strong> Acompanhe o processo de raciocínio do agente</li>
                  <li><strong>Detalhes:</strong> Validações individuais e queries geradas</li>
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">💡 Ative Tavily para informações atuais</CardTitle>
              </CardHeader>
              <CardContent className="text-sm">
                <p>Para perguntas sobre eventos recentes, tecnologias emergentes ou dados atualizados, marque a opção "Usar Tavily API" para obter resultados de busca reais.</p>
                <p className="text-muted-foreground mt-2">Sem Tavily, o agente simula resultados baseado no conhecimento do modelo de IA.</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">📥 Baixe e compartilhe relatórios</CardTitle>
              </CardHeader>
              <CardContent className="text-sm">
                <p>Use o botão "Baixar Relatório" para salvar os resultados em formato Markdown (.md). Você pode então:</p>
                <ul className="list-disc list-inside space-y-1 mt-2">
                  <li>Abrir em editores como Obsidian, Notion, ou VSCode</li>
                  <li>Converter para PDF usando ferramentas online</li>
                  <li>Compartilhar com colegas ou incluir em documentação</li>
                </ul>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  )
}
