// filepath: c:\Users\mohit\Desktop\python\MEDICAL RAG CHATBOT\medical_rag_chatbot\app\Frontend\src\components\ChatHistory.jsx
import { useEffect, useRef } from 'react'
import ChatBubble from './ChatBubble'
import LoadingBubble from './LoadingBubble'
import { cn } from '@components/lib/utils'

export default function ChatHistory({ messages, isLoading, className }) {
  const scrollAreaRef = useRef(null)

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [messages, isLoading])

  return (
    <div
      ref={scrollAreaRef}
      className={cn('space-y-6 overflow-y-auto p-4', className)}
    >
      {messages.map((msg, index) => (
        <ChatBubble key={index} role={msg.role} content={msg.content} />
      ))}
      {isLoading && <LoadingBubble />}
    </div>
  )
}