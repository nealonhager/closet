const API_BASE_URL = '/api'

export interface ProcessedFile {
  filename: string
  download_url: string
  size: number
  created: number
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

export const api = {
  async processImage(file: File, article: string): Promise<ProcessResponse> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('article', article)

    const response = await fetch(`${API_BASE_URL}/process`, {
      method: 'POST',
      body: formData,
    })

    return response.json()
  },

  async listProcessedFiles(): Promise<ListFilesResponse> {
    const response = await fetch(`${API_BASE_URL}/list-processed`)
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
    return response.json()
  }
}
