'use client'

import { useState, useEffect } from 'react'

interface AnalyticsData {
  totalConversations: number
  avgMessagesPerConversation: number
  activeUsers: number
  totalMessages: number
  newUsers: number
  periodDays: number
  retrievalCount: number
  avgLatency: number
  userCount: number
  leadCount: number
}

export default function Dashboard() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        // Fetch all analytics data from correct endpoints
        const [userEngagement, conversationStats, ragMetrics, crmInsights] = await Promise.all([
          fetch('http://localhost:8000/analytics/user-engagement').then(res => res.json()),
          fetch('http://localhost:8000/analytics/conversation-stats').then(res => res.json()),
          fetch('http://localhost:8000/analytics/rag-metrics').then(res => res.json()),
          fetch('http://localhost:8000/analytics/crm-insights').then(res => res.json())
        ])

        // Combine all analytics data
        const combinedAnalytics = {
          activeUsers: userEngagement.active_users || 0,
          totalMessages: userEngagement.total_messages || 0,
          newUsers: userEngagement.new_users || 0,
          periodDays: userEngagement.period_days || 0,
          totalConversations: conversationStats.total_conversations || 0,
          avgMessagesPerConversation: conversationStats.avg_messages_per_conversation || 0,
          retrievalCount: ragMetrics.retrieval_count || 0,
          avgLatency: ragMetrics.avg_latency || 0,
          userCount: crmInsights.user_count || 0,
          leadCount: crmInsights.lead_count || 0
        }

        setAnalytics(combinedAnalytics)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load analytics')
      } finally {
        setLoading(false)
      }
    }

    fetchAnalytics()
  }, [])

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
        <h3 className="text-red-800 font-semibold">Error Loading Analytics</h3>
        <p className="text-red-600 mt-2">{error}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Real-time analytics and insights</p>
      </div>

      {analytics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* User Engagement */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Users</p>
                <p className="text-2xl font-semibold text-gray-900">{analytics.activeUsers}</p>
              </div>
            </div>
          </div>

          {/* Total Messages */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Messages</p>
                <p className="text-2xl font-semibold text-gray-900">{analytics.totalMessages}</p>
              </div>
            </div>
          </div>

          {/* Conversations */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Conversations</p>
                <p className="text-2xl font-semibold text-gray-900">{analytics.totalConversations}</p>
              </div>
            </div>
          </div>

          {/* New Users */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-orange-100 rounded-lg">
                <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">New Users</p>
                <p className="text-2xl font-semibold text-gray-900">{analytics.newUsers}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Additional Stats */}
      {analytics && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h3>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Avg Messages per Conversation</span>
                <span className="font-semibold">{analytics.avgMessagesPerConversation.toFixed(1)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">RAG Retrievals</span>
                <span className="font-semibold">{analytics.retrievalCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Avg Response Time</span>
                <span className="font-semibold">{analytics.avgLatency.toFixed(2)}ms</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">CRM Insights</h3>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Users</span>
                <span className="font-semibold">{analytics.userCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Total Leads</span>
                <span className="font-semibold">{analytics.leadCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Period (Days)</span>
                <span className="font-semibold">{analytics.periodDays}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
