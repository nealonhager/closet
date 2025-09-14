import { useState } from 'react'
import { EyeIcon, ArrowDownTrayIcon, CalendarIcon, XMarkIcon, UserGroupIcon } from '@heroicons/react/24/outline'
import { Outfit } from '../utils/api'

interface OutfitsGalleryProps {
  outfits: Outfit[]
}

export function OutfitsGallery({ outfits }: OutfitsGalleryProps) {
  const [selectedOutfit, setSelectedOutfit] = useState<Outfit | null>(null)

  const formatDate = (timestamp: string) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleDownload = async (outfit: Outfit) => {
    try {
      const response = await fetch(`/api${outfit.download_url}`)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = outfit.filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  if (outfits.length === 0) {
    return (
      <div className="text-center py-12">
        <UserGroupIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">No outfits generated</h3>
        <p className="mt-1 text-sm text-gray-500">
          Select clothing items and generate outfits to see them here.
        </p>
      </div>
    )
  }

  return (
    <>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {outfits.map((outfit) => (
          <div key={outfit.filename} className="card">
            <div className="aspect-w-16 aspect-h-9 bg-gray-200">
              <img
                src={`/api${outfit.outfit_url}`}
                alt={outfit.filename}
                className="w-full h-48 object-cover cursor-pointer hover:opacity-75 transition-opacity"
                onClick={() => setSelectedOutfit(outfit)}
              />
            </div>
            <div className="p-4">
              <h3 className="text-sm font-medium text-gray-900 truncate">
                {outfit.filename}
              </h3>
              <div className="mt-2 flex items-center text-xs text-gray-500">
                <CalendarIcon className="h-4 w-4 mr-1" />
                {formatDate(outfit.created)}
              </div>
              {outfit.description && (
                <p className="mt-2 text-xs text-gray-600 line-clamp-2">
                  {outfit.description}
                </p>
              )}
              <div className="mt-3 flex space-x-2">
                <button
                  onClick={() => setSelectedOutfit(outfit)}
                  className="flex-1 btn-secondary text-xs"
                >
                  <EyeIcon className="h-4 w-4 mr-1" />
                  View
                </button>
                <button
                  onClick={() => handleDownload(outfit)}
                  className="flex-1 btn-primary text-xs"
                >
                  <ArrowDownTrayIcon className="h-4 w-4 mr-1" />
                  Download
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Outfit Modal */}
      {selectedOutfit && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75" onClick={() => setSelectedOutfit(null)}></div>
            <div className="relative bg-white rounded-lg max-w-4xl max-h-full">
              <div className="p-4">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-medium text-gray-900">
                    {selectedOutfit.filename}
                  </h3>
                  <button
                    onClick={() => setSelectedOutfit(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>
                
                {/* Main outfit image */}
                <div className="mb-4">
                  <img
                    src={`/api${selectedOutfit.outfit_url}`}
                    alt={selectedOutfit.filename}
                    className="max-w-full max-h-96 object-contain mx-auto"
                  />
                </div>

                {/* Outfit details */}
                <div className="mt-4 flex items-center text-sm text-gray-500">
                  <CalendarIcon className="h-4 w-4 mr-1" />
                  {formatDate(selectedOutfit.created)}
                </div>

                {selectedOutfit.description && (
                  <div className="mt-2">
                    <p className="text-sm text-gray-700">{selectedOutfit.description}</p>
                  </div>
                )}

                {/* Individual clothing items */}
                {selectedOutfit.items && selectedOutfit.items.length > 0 && (
                  <div className="mt-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">
                      Clothing Items ({selectedOutfit.items.length})
                    </h4>
                    <div className="grid grid-cols-2 gap-2">
                      {selectedOutfit.items.map((item) => (
                        <div key={item.id} className="flex items-center space-x-2 p-2 bg-gray-50 rounded">
                          <img
                            src={`/api${item.image_url}`}
                            alt={item.filename}
                            className="w-8 h-8 object-cover rounded"
                          />
                          <span className="text-xs text-gray-600 truncate">
                            {item.filename}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="mt-4 flex justify-end">
                  <button
                    onClick={() => handleDownload(selectedOutfit)}
                    className="btn-primary"
                  >
                    <ArrowDownTrayIcon className="h-4 w-4 mr-2" />
                    Download Outfit
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
