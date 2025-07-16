// filepath: c:\Users\mohit\Desktop\python\MEDICAL RAG CHATBOT\medical_rag_chatbot\app\Frontend\src\components\ChatInput.jsx
import { useState } from 'react'
import Textarea from 'react-textarea-autosize'
import { Icons } from './icons'
import { cn } from '@components/lib/utils'

export default function ChatInput({ onSend, isLoading, className }) {
  const [inputValue, setInputValue] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (isLoading || !inputValue.trim()) return
    onSend(inputValue)
    setInputValue('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div
      className={cn(
        'sticky bottom-0 w-full border-t border-border/40 bg-background/95 p-4 backdrop-blur supports-[backdrop-filter]:bg-background/60',
        className,
      )}
    >
      <form
        onSubmit={handleSubmit}
        className="relative mx-auto max-w-2xl rounded-2xl border border-input bg-background shadow-lg"
      >
        <Textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a medical question..."
          className="w-full resize-none rounded-2xl border-none bg-transparent p-4 pr-12 text-base text-foreground placeholder:text-muted-foreground focus:ring-0"
          minRows={1}
          maxRows={5}
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          className="absolute bottom-2.5 right-2.5 flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground transition-colors disabled:bg-muted disabled:text-muted-foreground"
        >
          <Icons.Send className="h-4 w-4" />
        </button>
      </form>
    </div>
  )
}