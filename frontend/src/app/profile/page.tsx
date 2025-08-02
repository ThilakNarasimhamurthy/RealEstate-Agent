'use client'

import { useState, useEffect } from 'react'

interface Conversation {
  _id: string
  user_id: string
  created_at: string
  updated_at: string
  message_count: number
}

interface Message {
  _id: string
  conversation_id: string
  role: string
  content: string
  timestamp: string
}

interface UserProfile {
  _id: string
  email: string
  name?: string
  company?: string
  created_at: string
  conversation_count: number
  total_messages: number
}

export default function Profile() {
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [selectedConversation, setSelectedConversation] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        // For demo purposes, create a mock profile
        const mockProfile: UserProfile = {
          _id: 'user_123',
          email: 'user@example.com',
          name: 'John Doe',
          company: 'Acme Corp',
          created_at: new Date().toISOString(),
          conversation_count: 5,
          total_messages: 23
        }
        setProfile(mockProfile)

        // Mock conversations
        const mockConversations: Conversation[] = [
          {
            _id: 'conv_1',
            user_id: 'user_123',
            created_at: new Date(Date.now() - 86400000).toISOString(),
            updated_at: new Date().toISOString(),
            message_count: 8
          },
          {
            _id: 'conv_2',
            user_id: 'user_123',
            created_at: new Date(Date.now() - 172800000).toISOString(),
            updated_at: new Date(Date.now() - 86400000).toISOString(),
            message_count: 5
          }
        ]
        setConversations(mockConversations)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load profile')
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [])

  const fetchMessages = async (conversationId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/conversations/${conversationId}/messages`)
      if (!response.ok) {
        throw new Error('Failed to fetch messages')
      }
      const data = await response.json()
      setMessages(data)
    } catch (err) {
      console.error('Error fetching messages:', err)
      // For demo, show mock messages
      const mockMessages: Message[] = [
        {
          _id: 'msg_1',
          conversation_id: conversationId,
          role: 'user',
          content: 'I\'m looking for a 3-bedroom house in downtown area.',
          timestamp: new Date(Date.now() - 3600000).toISOString()
        },
        {
          _id: 'msg_2',
          conversation_id: conversationId,
          role: 'assistant',
          content: 'I found several 3-bedroom properties in the downtown area. Would you like me to show you the details?',
          timestamp: new Date(Date.now() - 3500000).toISOString()
        }
      ]
      setMessages(mockMessages)
    }
  }

  const handleConversationClick = (conversationId: string) => {
    setSelectedConversation(conversationId)
    fetchMessages(conversationId)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <h3 className="text-red-800 font-semibold">Error Loading Profile</h3>
        <p className="text-red-600 mt-2">{error}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">User Profile</h1>
        <p className="text-gray-600 mt-2">Manage your account and view conversation history</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Information */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="text-center mb-6">
              <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h2 className="text-xl font-semibold text-gray-900">{profile?.name || 'User'}</h2>
              <p className="text-gray-600">{profile?.email}</p>
              {profile?.company && (
                <p className="text-sm text-gray-500 mt-1">{profile.company}</p>
              )}
            </div>

            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Member since</span>
                <span className="font-medium">{formatDate(profile?.created_at || '')}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Conversations</span>
                <span className="font-medium">{profile?.conversation_count}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Total messages</span>
                <span className="font-medium">{profile?.total_messages}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Conversation History */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Conversation History</h3>
            </div>
            
            <div className="divide-y divide-gray-200">
              {conversations.map((conversation) => (
                <div
                  key={conversation._id}
                  className={`px-6 py-4 cursor-pointer hover:bg-gray-50 transition-colors ${
                    selectedConversation === conversation._id ? 'bg-blue-50' : ''
                  }`}
                  onClick={() => handleConversationClick(conversation._id)}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        Conversation {conversation._id.slice(-4)}
                      </p>
                      <p className="text-xs text-gray-500">
                        {formatDate(conversation.updated_at)}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-gray-500">
                        {conversation.message_count} messages
                      </span>
                      <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Messages for Selected Conversation */}
          {selectedConversation && messages.length > 0 && (
            <div className="mt-6 bg-white rounded-lg shadow-sm border">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Messages</h3>
              </div>
              
              <div className="p-6 space-y-4">
                {messages.map((message) => (
                  <div
                    key={message._id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <p className="text-sm">{message.content}</p>
                      <p className={`text-xs mt-1 ${
                        message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                      }`}>
                        {formatDate(message.timestamp)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
} 