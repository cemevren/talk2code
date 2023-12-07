import { MessageForm } from './components/chat-message-form'
import { useState } from 'react'
import { TooltipProvider } from './components/ui/tooltip'
import { Message } from './types'
import { Separator } from '@/components/ui/separator'
import { ChatMessage } from './components/chat-message'


function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [listening, setListening] = useState(false)

  const statusMessage = {
    subscribed: 'Subscribed',
    unsubscribed: 'Unsubscribed'
  }

  const onSubmit = async (value: string) => {
    const fetchData = async () => {
      setMessages(messages => [...messages, { content: value, role: 'user' }])

      const response = await fetch('/completion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_message: value, id: 'id' })
      })

      if (response.body) {
        const reader = response.body.getReader()
        const decoder = new TextDecoder()

        setMessages(messages => [
          ...messages,
          { content: '', role: 'assistant' }
        ])

        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          const chunk = decoder.decode(value)
          setMessages(messages => {
            const newMessages = [...messages]
            const lastMessageIndex = newMessages.length - 1
            newMessages[lastMessageIndex] = {
              ...newMessages[lastMessageIndex],
              content: newMessages[lastMessageIndex].content + chunk
            }
            return newMessages
          })
        }
      }
    }

    fetchData()
  }

  return (
    <>
      <TooltipProvider>
        <div className="flex flex-col h-screen">
          <header className="bg-white p-4 flex justify-center items-center border-b">
            <h1 className="text-lg text-slate-900 w-min font-bold">
              Talk2Code
            </h1>
          </header>
          <div className="flex flex-col h-screen bg-muted/50">
            <div className="flex-1 overflow-y-auto p-4">
              <div className="mx-auto sm:max-w-4xl sm:px-4">
                {messages.map((message, index) => (
                  <div key={index}>
                    <ChatMessage message={message} />
                    {index < messages.length - 1 && (
                      <Separator className="my-4 md:my-8" />
                    )}
                  </div>
                ))}
              </div>
            </div>
            <div className="p-4">
              <div className="mx-auto sm:max-w-4xl">
                <MessageForm
                  input={input}
                  setInput={setInput}
                  onSubmit={onSubmit}
                  isLoading={isLoading}
                />
              </div>
            </div>
          </div>
        </div>
      </TooltipProvider>
    </>
  )
}

export default App
