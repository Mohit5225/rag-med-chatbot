// filepath: c:\Users\mohit\Desktop\python\MEDICAL RAG CHATBOT\medical_rag_chatbot\app\Frontend\src\components\ChatBubble.jsx
import { Icons } from './icons'
import { cn } from '@components/lib/utils'
import ReactMarkdown from 'react-markdown'

export default function ChatBubble({ role, content }) {
  const isUser = role === 'user'
  const Icon = isUser ? Icons.User : Icons.Bot

  return (
    <div
      className={cn(
        'flex items-start gap-4 rounded-lg p-4',
        isUser ? 'justify-end' : 'bg-muted/50',
      )}
    >
      {!isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
          <Icon className="h-5 w-5" />
        </div>
      )}
      <div
        className={cn(
          'prose prose-sm max-w-full break-words dark:prose-invert',
          isUser && 'text-right',
        )}
      >
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
      {isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent text-accent-foreground">
          <Icon className="h-5 w-5" />
        </div>
      )}
    </div>
  )
}