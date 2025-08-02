import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Multi-Agentic AI Real Estate Assistant',
  description: 'Intelligent real estate assistant with RAG, CRM, and conversational AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex h-screen bg-gray-50">
          {/* Sidebar */}
          <div className="w-64 bg-white shadow-lg">
            <div className="p-6">
              <h1 className="text-2xl font-bold text-gray-800 mb-8">AI Assistant</h1>
              <nav className="space-y-2">
                <a href="/" className="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">
                  Dashboard
                </a>
                <a href="/chat" className="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">
                  Chat
                </a>
                <a href="/documents" className="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">
                  Documents
                </a>
                <a href="/profile" className="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors">
                  Profile
                </a>
              </nav>
            </div>
          </div>
          
          {/* Main Content */}
          <div className="flex-1 overflow-auto">
            <main className="p-8">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  )
}
