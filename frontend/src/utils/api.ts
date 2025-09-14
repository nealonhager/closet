const API_BASE_URL = '/api'

export interface ProcessedFile {
  id: number
  filename: string
  download_url: string
  image_url: string
  description?: string
  categories: string[]
  tags: string[]
  created: string
  updated: string
}

export interface ProcessResponse {
  success: boolean
  message: string
  output_file?: string
  download_url?: string
  error?: string
}

export interface ListFilesResponse {
  files: ProcessedFile[]
  count: number
}

export interface GenerateOutfitResponse {
  success: boolean
  message: string
  outfit_url?: string
  error?: string
}

export interface OutfitItem {
  id: number
  filename: string
  image_url: string
}

export interface Outfit {
  id: number
  filename: string
  download_url: string
  outfit_url: string
  description?: string
  created: string
  updated: string
  items: OutfitItem[]
}

export interface ListOutfitsResponse {
  outfits: Outfit[]
  count: number
}

export const api = {
  async processImage(file: File, article: string): Promise<ProcessResponse> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('article', article)

    const response = await fetch(`${API_BASE_URL}/process`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Network error' }))
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`)
    }

    return response.json()
  },

  async listProcessedFiles(): Promise<ListFilesResponse> {
    const response = await fetch(`${API_BASE_URL}/list-processed`)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Network error' }))
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`)
    }
    
    return response.json()
  },

  async downloadFile(filename: string): Promise<Blob> {
    const response = await fetch(`${API_BASE_URL}/download/${filename}`)
    if (!response.ok) {
      throw new Error('Failed to download file')
    }
    return response.blob()
  },

  async healthCheck(): Promise<{ status: string; message: string }> {
    const response = await fetch(`${API_BASE_URL}/health`)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Network error' }))
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`)
    }
    
    return response.json()
  },

  async generateOutfit(selectedFiles: ProcessedFile[]): Promise<GenerateOutfitResponse> {
    const response = await fetch(`${API_BASE_URL}/generate-outfit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image_ids: selectedFiles.map(file => file.id)
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Network error' }))
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`)
    }

    return response.json()
  },

  async listOutfits(): Promise<ListOutfitsResponse> {
    const response = await fetch(`${API_BASE_URL}/list-outfits`)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Network error' }))
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`)
    }
    
    return response.json()
  }
}
