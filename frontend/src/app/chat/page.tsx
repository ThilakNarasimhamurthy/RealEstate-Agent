'use client'

import { useState, useEffect, useRef } from 'react'

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  rag_sources?: { content: string; score?: number }[];
}

interface ChatResponse {
  response: string
  user_id: string
  conversation_id: string
  extracted_info: any
  rag_sources: any[]
  crm_actions: any[]
  properties: any[]
  conversation_history: any[]
}

function parsePropertyContent(content: string) {
  const fields: Record<string, string> = {};
  content.split(",").forEach((part) => {
    const [key, ...rest] = part.split(":");
    if (key && rest.length) fields[key.trim()] = rest.join(":").trim();
  });
  return fields;
}

function PropertyCard({ property }: { property: { content: string; score?: number } }) {
  const fields = parsePropertyContent(property.content);
  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 shadow-md rounded-lg p-4 mb-3 border border-blue-200 hover:shadow-lg transition-shadow">
      <div className="font-bold text-lg mb-3 text-blue-900 border-b border-blue-200 pb-2">
        {fields["Property Address"] || fields["Address"] || "Property"}
      </div>
      <div className="grid grid-cols-2 gap-3 text-xs">
        {Object.entries(fields).map(([key, value]) =>
          key !== "Property Address" && key !== "Address" ? (
            <div key={key} className="flex flex-col bg-white rounded-md p-2 shadow-sm">
              <span className="text-gray-600 text-xs font-medium uppercase tracking-wide">{key}</span>
              <span className="text-gray-900 font-semibold mt-1 text-sm">{value}</span>
            </div>
          ) : null
        )}
      </div>
      {property.score !== undefined && (
        <div className="mt-3 text-xs text-right">
          <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium">
            Relevance: {(property.score * 100).toFixed(1)}%
          </span>
        </div>
      )}
    </div>
  );
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [userId, setUserId] = useState('')
  const [conversationId, setConversationId] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Generate a unique user ID if not exists
    if (!userId) {
      setUserId(`user_${Date.now()}`)
    }
  }, [userId])

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          user_id: userId,
          conversation_id: conversationId
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to send message')
      }

      const data: ChatResponse = await response.json()
      
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
        // Add rag_sources if they exist in the response
        rag_sources: data.rag_sources && data.rag_sources.length > 0 ? data.rag_sources : undefined
      }

      setMessages(prev => [...prev, assistantMessage])
      setConversationId(data.conversation_id)

      // Log extracted info and properties for debugging
      if (data.extracted_info) {
        console.log('Extracted Info:', data.extracted_info)
      }
      if (data.rag_sources && data.rag_sources.length > 0) {
        console.log('RAG Sources Found:', data.rag_sources)
      }

    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Chat with AI Assistant</h1>
        <p className="text-gray-600 mt-2">Ask me about real estate, properties, or anything else!</p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 bg-gradient-to-b from-gray-50 to-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <div className="h-full flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 py-12">
                <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <p className="text-lg font-medium">Start a conversation by typing a message below</p>
                <p className="text-sm mt-2">Try asking about properties, real estate, or just say hello!</p>
              </div>
            )}

            {messages.map((msg, idx) => {
              // For assistant messages, show both conversational response and property cards
              if (msg.role === 'assistant') {
                return (
                  <div key={idx} className="flex flex-col gap-3 my-3">
                    {/* Show the conversational response as a chat bubble */}
                    <div className="flex justify-start">
                      <div className="bg-white shadow-md rounded-2xl px-6 py-4 max-w-[80%] border border-gray-100">
                        <p className="text-gray-800 leading-relaxed">{msg.content}</p>
                      </div>
                    </div>
                    
                    {/* Show property cards if rag_sources exist */}
                    {msg.rag_sources && Array.isArray(msg.rag_sources) && msg.rag_sources.length > 0 && (
                      <div className="mt-3">
                        {msg.rag_sources.map((property: { content: string; score?: number }, i: number) => (
                          <PropertyCard key={i} property={property} />
                        ))}
                      </div>
                    )}
                  </div>
                );
              }
              
              // For user messages, render as chat bubble
              return (
                <div key={idx} className="flex justify-end my-3">
                  <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg rounded-2xl px-6 py-4 max-w-[80%]">
                    <p className="leading-relaxed">{msg.content}</p>
                  </div>
                </div>
              );
            })}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-white shadow-md rounded-2xl px-6 py-4 border border-gray-100">
                  <div className="flex items-center space-x-3">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                    <span className="text-gray-700 font-medium">AI is thinking...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 bg-white p-6">
            <div className="flex space-x-4">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message here..."
                className="flex-1 px-6 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800 placeholder-gray-500 bg-white shadow-sm transition-all duration-200"
                disabled={loading}
              />
              <button
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl font-medium"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* User Info */}
      <div className="mt-4 text-sm text-gray-500 bg-gray-50 rounded-lg p-3">
        <span className="font-medium">User ID:</span> {userId}
        {conversationId && (
          <span className="ml-4">
            <span className="font-medium">Conversation ID:</span> {conversationId}
          </span>
        )}
      </div>
    </div>
  )
} 