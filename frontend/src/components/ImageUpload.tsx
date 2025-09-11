import { useState, useRef } from 'react'
import { CloudArrowUpIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { api } from '../utils/api'

interface ImageUploadProps {
  onProcessed: () => void
  onError: (error: string) => void
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
}

export function ImageUpload({ onProcessed, onError, isLoading, setIsLoading }: ImageUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [article, setArticle] = useState('')
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleFile = (file: File) => {
    if (file.type.startsWith('image/')) {
      setSelectedFile(file)
    } else {
      onError('Please select a valid image file')
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const removeFile = () => {
    setSelectedFile(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!selectedFile || !article.trim()) {
      onError('Please select a file and enter an article type')
      return
    }

    setIsLoading(true)
    try {
      const response = await api.processImage(selectedFile, article.trim())
      
      if (response.success) {
        onProcessed()
        setSelectedFile(null)
        setArticle('')
        if (fileInputRef.current) {
          fileInputRef.current.value = ''
        }
      } else {
        onError(response.message || 'Processing failed')
      }
    } catch (err) {
      onError('Failed to process image. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* File Upload Area */}
      <div
        className={`relative border-2 border-dashed rounded-lg p-6 ${
          dragActive
            ? 'border-primary-400 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileInput}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        
        <div className="text-center">
          <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
          <div className="mt-4">
            <label className="cursor-pointer">
              <span className="mt-2 block text-sm font-medium text-gray-900">
                {selectedFile ? selectedFile.name : 'Drop your image here, or click to select'}
              </span>
              <span className="mt-1 block text-sm text-gray-500">
                PNG, JPG, JPEG up to 16MB
              </span>
            </label>
          </div>
        </div>
      </div>

      {/* Selected File Preview */}
      {selectedFile && (
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
          <div className="flex items-center">
            <img
              src={URL.createObjectURL(selectedFile)}
              alt="Preview"
              className="h-10 w-10 object-cover rounded"
            />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
              <p className="text-sm text-gray-500">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={removeFile}
            className="text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>
      )}

      {/* Article Type Input */}
      <div>
        <label htmlFor="article" className="block text-sm font-medium text-gray-700">
          Article Type
        </label>
        <input
          type="text"
          id="article"
          value={article}
          onChange={(e) => setArticle(e.target.value)}
          placeholder="e.g., sweater, shirt, pants, dress..."
          className="input-field mt-1"
          disabled={isLoading}
        />
        <p className="mt-1 text-sm text-gray-500">
          What type of clothing item is in the image?
        </p>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={!selectedFile || !article.trim() || isLoading}
        className="btn-primary w-full"
      >
        {isLoading ? (
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            Processing...
          </div>
        ) : (
          'Process Image'
        )}
      </button>
    </form>
  )
}
