// filepath: c:\Users\mohit\Desktop\python\MEDICAL RAG CHATBOT\medical_rag_chatbot\app\Frontend\src\App.jsx
import Header from '@components/Header'
import ChatHistory from '@components/ChatHistory'
import ChatInput from '@components/ChatInput'
import { useChat } from '@hooks/useChat'

function App() {
  const { messages, isLoading, sendMessage, resetChat } = useChat()

  return (
    <div className="flex h-screen flex-col bg-background">
      <Header onReset={resetChat} />
      <main className="relative flex-1 overflow-hidden">
        <div className="absolute inset-0 flex flex-col">
          <ChatHistory
            messages={messages}
            isLoading={isLoading}
            className="flex-1"
          />
          <ChatInput onSend={sendMessage} isLoading={isLoading} />
        </div>
      </main>
    </div>
  )
}

export default App