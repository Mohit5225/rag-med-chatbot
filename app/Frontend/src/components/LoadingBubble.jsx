// filepath: c:\Users\mohit\Desktop\python\MEDICAL RAG CHATBOT\medical_rag_chatbot\app\Frontend\src\components\LoadingBubble.jsx
import { Icons } from './icons'

export default function LoadingBubble() {
  return (
    <div className="flex items-start gap-4 rounded-lg bg-muted/50 p-4">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground">
        <Icons.Bot className="h-5 w-5" />
      </div>
      <div className="flex items-center gap-1 pt-2">
        <span className="h-2 w-2 animate-[bounce_1s_infinite] rounded-full bg-muted-foreground"></span>
        <span className="h-2 w-2 animate-[bounce_1s_infinite_200ms] rounded-full bg-muted-foreground"></span>
        <span className="h-2 w-2 animate-[bounce_1s_infinite_400ms] rounded-full bg-muted-foreground"></span>
      </div>
    </div>
  )
}