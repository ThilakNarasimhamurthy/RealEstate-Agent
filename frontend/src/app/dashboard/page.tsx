'use client'

import { useState, useEffect } from 'react'

interface AnalyticsData {
  userEngagement?: {
    active_users: number
    total_messages: number
    new_users: number
    period_days: number
  }
  conversationStats?: {
    total_conversations: number
    avg_messages_per_conversation: number
  }
  ragMetrics?: {
    retrieval_count: number
    avg_latency: number
  }
  crmInsights?: {
    user_count: number
    lead_count: number
  }
}

export default function Dashboard() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true)
        
        // Fetch all analytics data in parallel
        const [userEngagement, conversationStats, ragMetrics, crmInsights] = await Promise.all([
          fetch('http://localhost:8000/analytics/user-engagement').then(res => res.json()),
          fetch('http://localhost:8000/analytics/conversation-stats').then(res => res.json()),
          fetch('http://localhost:8000/analytics/rag-metrics').then(res => res.json()),
          fetch('http://localhost:8000/analytics/crm-insights').then(res => res.json())
        ])

        setAnalyticsData({
          userEngagement,
          conversationStats,
          ragMetrics,
          crmInsights
        })
      } catch (err) {
        console.error('Error fetching analytics:', err)
        setError('Failed to load analytics data')
      } finally {
        setLoading(false)
      }
    }

    fetchAnalytics()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Error Loading Dashboard</h2>
          <p className="text-gray-600">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="text-gray-600 mt-2">Real-time insights into your AI assistant performance</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* User Engagement */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Users</p>
                <p className="text-2xl font-bold text-gray-900">{analyticsData.userEngagement?.active_users || 0}</p>
              </div>
            </div>
          </div>

          {/* Total Messages */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Messages</p>
                <p className="text-2xl font-bold text-gray-900">{analyticsData.userEngagement?.total_messages || 0}</p>
              </div>
            </div>
          </div>

          {/* Conversations */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Conversations</p>
                <p className="text-2xl font-bold text-gray-900">{analyticsData.conversationStats?.total_conversations || 0}</p>
              </div>
            </div>
          </div>

          {/* RAG Retrievals */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <div className="flex items-center">
              <div className="p-2 bg-orange-100 rounded-lg">
                <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">RAG Retrievals</p>
                <p className="text-2xl font-bold text-gray-900">{analyticsData.ragMetrics?.retrieval_count || 0}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Additional Metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          {/* CRM Insights */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">CRM Insights</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Total Users</span>
                <span className="font-semibold text-gray-900">{analyticsData.crmInsights?.user_count || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Total Leads</span>
                <span className="font-semibold text-gray-900">{analyticsData.crmInsights?.lead_count || 0}</span>
              </div>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Avg Messages/Conversation</span>
                <span className="font-semibold text-gray-900">
                  {analyticsData.conversationStats?.avg_messages_per_conversation?.toFixed(1) || 0}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Avg RAG Latency</span>
                <span className="font-semibold text-gray-900">
                  {analyticsData.ragMetrics?.avg_latency?.toFixed(2) || 0}ms
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 