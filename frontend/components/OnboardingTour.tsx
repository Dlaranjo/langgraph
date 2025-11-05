"use client"

import { useState, useEffect } from "react"
import { Rocket, ArrowRight, Check } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

interface OnboardingStep {
  title: string
  description: string
  image?: string
  icon: React.ReactNode
}

const ONBOARDING_STEPS: OnboardingStep[] = [
  {
    title: "Bem-vindo ao Agente Pesquisador IA! 🎉",
    description: "Uma ferramenta inteligente que pesquisa, valida e gera relatórios confiáveis automaticamente. Vamos fazer um tour rápido?",
    icon: <Rocket className="h-12 w-12 text-purple-600" />
  },
  {
    title: "1. Configure suas API Keys 🔑",
    description: "Você precisará de uma ANTHROPIC_API_KEY (obrigatória) para usar o Claude. Opcionalmente, adicione uma TAVILY_API_KEY para buscas web reais.",
    icon: <div className="text-6xl">🔑</div>
  },
  {
    title: "2. Faça uma pergunta específica 💭",
    description: "Digite sua pergunta na área de texto. Quanto mais específica, melhores os resultados! Você pode usar nossos exemplos para começar.",
    icon: <div className="text-6xl">💭</div>
  },
  {
    title: "3. Configure as iterações ⚙️",
    description: "Escolha quantos ciclos de busca e validação deseja. 1 iteração é rápida, 3 iterações é mais completa e confiável.",
    icon: <div className="text-6xl">⚙️</div>
  },
  {
    title: "4. Explore os resultados 📊",
    description: "Veja o relatório completo, fontes consultadas, métricas de confiança e detalhes da validação nas diferentes tabs.",
    icon: <div className="text-6xl">📊</div>
  },
  {
    title: "Pronto para começar! 🚀",
    description: "Agora você está pronto para usar o Agente Pesquisador IA. Se precisar de ajuda, clique no botão 'Ajuda' no topo da página.",
    icon: <Check className="h-12 w-12 text-green-600" />
  }
]

const STORAGE_KEY = "agente-pesquisador-onboarding-completed"

export function OnboardingTour() {
  const [open, setOpen] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)

  useEffect(() => {
    // Verifica se o usuário já viu o onboarding
    const hasSeenOnboarding = localStorage.getItem(STORAGE_KEY)
    if (!hasSeenOnboarding) {
      // Pequeno delay para melhor experiência
      const timer = setTimeout(() => setOpen(true), 500)
      return () => clearTimeout(timer)
    }
  }, [])

  const handleComplete = () => {
    localStorage.setItem(STORAGE_KEY, "true")
    setOpen(false)
    setCurrentStep(0)
  }

  const handleSkip = () => {
    localStorage.setItem(STORAGE_KEY, "true")
    setOpen(false)
    setCurrentStep(0)
  }

  const handleNext = () => {
    if (currentStep < ONBOARDING_STEPS.length - 1) {
      setCurrentStep(currentStep + 1)
    } else {
      handleComplete()
    }
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const currentStepData = ONBOARDING_STEPS[currentStep]
  const isLastStep = currentStep === ONBOARDING_STEPS.length - 1

  const handleOpenChange = (newOpen: boolean) => {
    if (!newOpen) {
      // Quando o usuário fecha o modal (clica no X ou fora), marca como concluído
      handleSkip()
    } else {
      setOpen(newOpen)
    }
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="text-2xl">Tour Guiado</DialogTitle>
          <DialogDescription>
            Passo {currentStep + 1} de {ONBOARDING_STEPS.length}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Progress bar */}
          <div className="w-full bg-secondary rounded-full h-2">
            <div
              className="bg-gradient-to-r from-purple-600 to-pink-600 h-2 rounded-full transition-all duration-300"
              style={{
                width: `${((currentStep + 1) / ONBOARDING_STEPS.length) * 100}%`
              }}
            />
          </div>

          {/* Step content */}
          <Card className="border-2 border-purple-100">
            <CardContent className="pt-6">
              <div className="flex flex-col items-center text-center space-y-4">
                <div className="p-4 bg-purple-50 rounded-full">
                  {currentStepData.icon}
                </div>

                <h3 className="text-xl font-bold text-gray-900">
                  {currentStepData.title}
                </h3>

                <p className="text-muted-foreground max-w-md">
                  {currentStepData.description}
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Navigation buttons */}
          <div className="flex items-center justify-between pt-4">
            <Button
              variant="outline"
              onClick={handlePrevious}
              disabled={currentStep === 0}
            >
              Anterior
            </Button>

            <div className="flex gap-1">
              {ONBOARDING_STEPS.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentStep(index)}
                  className={`h-2 rounded-full transition-all ${
                    index === currentStep
                      ? "w-8 bg-purple-600"
                      : "w-2 bg-gray-300 hover:bg-gray-400"
                  }`}
                  aria-label={`Ir para passo ${index + 1}`}
                />
              ))}
            </div>

            <Button onClick={handleNext} className="gap-2">
              {isLastStep ? (
                <>
                  Começar
                  <Check className="h-4 w-4" />
                </>
              ) : (
                <>
                  Próximo
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          </div>

          {/* Skip button */}
          {!isLastStep && (
            <div className="text-center">
              <Button
                variant="link"
                onClick={handleSkip}
                className="text-muted-foreground"
              >
                Pular tour
              </Button>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}

// Hook para reabrir o tour manualmente
export function useOnboardingTour() {
  const resetOnboarding = () => {
    localStorage.removeItem(STORAGE_KEY)
    window.location.reload()
  }

  return { resetOnboarding }
}
