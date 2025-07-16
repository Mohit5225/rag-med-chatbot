// filepath: c:\Users\mohit\Desktop\python\MEDICAL RAG CHATBOT\medical_rag_chatbot\app\Frontend\src\hooks\useChat.js
import { useState, useCallback } from 'react'
import toast from 'react-hot-toast'

export function useChat() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = useCallback(async (messageContent) => {
    if (!messageContent.trim()) return

    const userMessage = { role: 'user', content: messageContent }
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: messageContent }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'An unknown error occurred')
      }

      const botMessage = { role: 'bot', content: '' }
      setMessages((prev) => [...prev, botMessage])

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let content = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        content += decoder.decode(value, { stream: true })
        setMessages((prev) =>
          prev.map((msg, i) =>
            i === prev.length - 1 ? { ...msg, content } : msg,
          ),
        )
      }
    } catch (error) {
      console.error('Chat API error:', error)
      toast.error(`Error: ${error.message}`)
      setMessages((prev) => prev.filter((_, i) => i !== prev.length - 1)) // Remove placeholder
    } finally {
      setIsLoading(false)
    }
  }, [])

  const resetChat = useCallback(() => {
    setMessages([])
    toast.success('Chat has been reset.')
  }, [])

  return { messages, isLoading, sendMessage, resetChat }
}