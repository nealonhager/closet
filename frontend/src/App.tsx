import { useState, useEffect } from 'react'
import { PhotoIcon, CloudArrowUpIcon, CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'
import { ImageUpload } from './components/ImageUpload'
import { ImageGallery } from './components/ImageGallery'
import { api, ProcessedFile } from './utils/api'

function App() {
  const [processedFiles, setProcessedFiles] = useState<ProcessedFile[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  const loadProcessedFiles = async () => {
    try {
      const response = await api.listProcessedFiles()
      setProcessedFiles(response.files)
    } catch (err) {
      setError('Failed to load processed files')
    }
  }

  useEffect(() => {
    loadProcessedFiles()
  }, [])

  const handleImageProcessed = () => {
    setSuccess('Image processed successfully!')
    loadProcessedFiles()
    setTimeout(() => setSuccess(null), 3000)
  }

  const handleError = (errorMessage: string) => {
    setError(errorMessage)
    setTimeout(() => setError(null), 5000)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <PhotoIcon className="h-8 w-8 text-primary-600" />
              <h1 className="ml-2 text-2xl font-bold text-gray-900">Closet AI</h1>
            </div>
            <div className="text-sm text-gray-500">
              Smart Wardrobe Management
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Status Messages */}
          {error && (
            <div className="mb-6 rounded-md bg-red-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">{error}</h3>
                </div>
              </div>
            </div>
          )}

          {success && (
            <div className="mb-6 rounded-md bg-green-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <CheckCircleIcon className="h-5 w-5 text-green-400" />
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-green-800">{success}</h3>
                </div>
              </div>
            </div>
          )}

          {/* Upload Section */}
          <div className="mb-8">
            <div className="card">
              <div className="px-4 py-5 sm:p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">
                  Upload & Process Images
                </h2>
                <ImageUpload
                  onProcessed={handleImageProcessed}
                  onError={handleError}
                  isLoading={isLoading}
                  setIsLoading={setIsLoading}
                />
              </div>
            </div>
          </div>

          {/* Gallery Section */}
          <div>
            <div className="card">
              <div className="px-4 py-5 sm:p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">
                  Processed Images ({processedFiles.length})
                </h2>
                <ImageGallery files={processedFiles} />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
