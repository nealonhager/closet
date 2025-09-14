import { useState } from 'react'
import { EyeIcon, ArrowDownTrayIcon, CalendarIcon, XMarkIcon, CheckIcon } from '@heroicons/react/24/outline'
import { ProcessedFile } from '../utils/api'

interface ImageGalleryProps {
  files: ProcessedFile[]
  onGenerateOutfit?: (selectedFiles: ProcessedFile[]) => void
}

export function ImageGallery({ files, onGenerateOutfit }: ImageGalleryProps) {
  const [selectedImage, setSelectedImage] = useState<ProcessedFile | null>(null)
  const [selectedFiles, setSelectedFiles] = useState<Set<string>>(new Set())
  const [isSelectMode, setIsSelectMode] = useState(false)


  const formatDate = (timestamp: string) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleDownload = async (file: ProcessedFile) => {
    try {
      const response = await fetch(`/api${file.download_url}`)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = file.filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  const toggleFileSelection = (filename: string) => {
    const newSelected = new Set(selectedFiles)
    if (newSelected.has(filename)) {
      newSelected.delete(filename)
    } else {
      newSelected.add(filename)
    }
    setSelectedFiles(newSelected)
  }

  const handleGenerateOutfit = () => {
    const selectedFileObjects = files.filter(file => selectedFiles.has(file.filename))
    if (onGenerateOutfit && selectedFileObjects.length > 0) {
      onGenerateOutfit(selectedFileObjects)
    }
  }

  const exitSelectMode = () => {
    setIsSelectMode(false)
    setSelectedFiles(new Set())
  }

  if (files.length === 0) {
    return (
      <div className="text-center py-12">
        <EyeIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">No processed images</h3>
        <p className="mt-1 text-sm text-gray-500">
          Upload and process some images to see them here.
        </p>
      </div>
    )
  }

  return (
    <>
      {/* Selection Controls */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {!isSelectMode ? (
            <button
              onClick={() => setIsSelectMode(true)}
              className="btn-secondary"
            >
              Select Items
            </button>
          ) : (
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">
                {selectedFiles.size} item{selectedFiles.size !== 1 ? 's' : ''} selected
              </span>
              <button
                onClick={exitSelectMode}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Cancel
              </button>
            </div>
          )}
        </div>
        
        {isSelectMode && selectedFiles.size > 0 && onGenerateOutfit && (
          <button
            onClick={handleGenerateOutfit}
            className="btn-primary"
          >
            Generate Outfit ({selectedFiles.size})
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {files.map((file) => {
          const isSelected = selectedFiles.has(file.filename)
          return (
            <div 
              key={file.filename} 
              className={`card relative ${isSelectMode ? 'cursor-pointer' : ''} ${
                isSelected ? 'ring-2 ring-blue-500 bg-blue-50' : ''
              }`}
              onClick={() => isSelectMode && toggleFileSelection(file.filename)}
            >
              {isSelectMode && (
                <div className="absolute top-2 right-2 z-10">
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                    isSelected 
                      ? 'bg-blue-500 border-blue-500' 
                      : 'bg-white border-gray-300'
                  }`}>
                    {isSelected && <CheckIcon className="w-4 h-4 text-white" />}
                  </div>
                </div>
              )}
              
              <div className="aspect-w-16 aspect-h-9 bg-gray-200">
                <img
                  src={`/api${file.image_url}`}
                  alt={file.filename}
                  className={`w-full h-48 object-cover transition-opacity ${
                    isSelectMode ? 'cursor-pointer hover:opacity-75' : 'cursor-pointer hover:opacity-75'
                  }`}
                  onClick={(e) => {
                    if (!isSelectMode) {
                      e.stopPropagation()
                      setSelectedImage(file)
                    }
                  }}
                />
              </div>
              <div className="p-4">
                <h3 className="text-sm font-medium text-gray-900 truncate">
                  {file.filename}
                </h3>
                <div className="mt-2 flex items-center text-xs text-gray-500">
                  <CalendarIcon className="h-4 w-4 mr-1" />
                  {formatDate(file.created)}
                </div>
                {!isSelectMode && (
                  <div className="mt-3 flex space-x-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        setSelectedImage(file)
                      }}
                      className="flex-1 btn-secondary text-xs"
                    >
                      <EyeIcon className="h-4 w-4 mr-1" />
                      View
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleDownload(file)
                      }}
                      className="flex-1 btn-primary text-xs"
                    >
                      <ArrowDownTrayIcon className="h-4 w-4 mr-1" />
                      Download
                    </button>
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {/* Image Modal */}
      {selectedImage && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75" onClick={() => setSelectedImage(null)}></div>
            <div className="relative bg-white rounded-lg max-w-4xl max-h-full">
              <div className="p-4">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-medium text-gray-900">
                    {selectedImage.filename}
                  </h3>
                  <button
                    onClick={() => setSelectedImage(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>
                <img
                  src={`/api${selectedImage.image_url}`}
                  alt={selectedImage.filename}
                  className="max-w-full max-h-96 object-contain mx-auto"
                />
                <div className="mt-4 flex items-center text-sm text-gray-500">
                  <CalendarIcon className="h-4 w-4 mr-1" />
                  {formatDate(selectedImage.created)}
                </div>
                <div className="mt-4 flex justify-end">
                  <button
                    onClick={() => handleDownload(selectedImage)}
                    className="btn-primary"
                  >
                    <ArrowDownTrayIcon className="h-4 w-4 mr-2" />
                    Download
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
