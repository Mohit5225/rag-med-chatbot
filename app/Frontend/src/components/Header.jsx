// filepath: c:\Users\mohit\Desktop\python\MEDICAL RAG CHATBOT\medical_rag_chatbot\app\Frontend\src\components\Header.jsx
import { Icons } from './icons'
import { cn } from '@components/lib/utils'

export default function Header({ onReset, className }) {
  return (
    <header
      className={cn(
        'sticky top-0 z-10 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60',
        className,
      )}
    >
      <div className="container flex h-14 max-w-screen-2xl items-center justify-between">
        <div className="flex items-center gap-2">
          <Icons.Bot className="h-6 w-6 text-primary" />
          <h1 className="text-lg font-semibold tracking-tight">
            Medical RAG Chatbot
          </h1>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={onReset}
            className="flex items-center gap-2 rounded-md p-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
          >
            <Icons.Reset className="h-4 w-4" />
            New Chat
          </button>
        </div>
      </div>
    </header>
  )
}