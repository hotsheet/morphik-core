/**
 * Documents API client
 * This module handles interaction with the document-related API endpoints
 */

import { createAuthHeaders } from './utils';

export interface Document {
  external_id: string;
  owner: Record<string, any>;
  content_type: string;
  filename: string | null;
  metadata: Record<string, any>;
  storage_info: Record<string, any>;
  storage_files: Array<{
    bucket: string;
    key: string;
    version: number;
    filename: string;
    content_type: string;
    timestamp: string;
  }>;
  system_metadata: Record<string, any>;
  additional_metadata: Record<string, any>;
  access_control: Record<string, any>;
  chunk_ids: string[];
}

/**
 * Update a document with text content
 * 
 * @param apiBaseUrl - Base URL for the API
 * @param documentId - ID of the document to update
 * @param text - New text content for the document
 * @param authToken - Authentication token
 * @param options - Optional parameters
 * @returns The updated document metadata
 */
export async function updateDocumentWithText(
  apiBaseUrl: string,
  documentId: string,
  text: string,
  authToken: string | null,
  options?: {
    filename?: string;
    metadata?: Record<string, any>;
    rules?: Array<Record<string, any>>;
    updateStrategy?: string;
    useColpali?: boolean;
  }
): Promise<Document> {
  try {
    let url = `${apiBaseUrl}/documents/${documentId}/update_text`;
    const queryParams: string[] = [];
    
    if (options?.useColpali !== undefined) {
      queryParams.push(`use_colpali=${options.useColpali}`);
    }
    
    if (queryParams.length > 0) {
      url += `?${queryParams.join('&')}`;
    }

    const requestBody: Record<string, any> = {
      text
    };
    
    if (options?.filename) {
      requestBody.filename = options.filename;
    }
    
    if (options?.metadata) {
      requestBody.metadata = JSON.stringify(options.metadata);
    }
    
    if (options?.rules) {
      requestBody.rules = JSON.stringify(options.rules);
    }
    
    if (options?.updateStrategy) {
      requestBody.update_strategy = options.updateStrategy;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: createAuthHeaders(authToken, 'application/json'),
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to update document with text: ${response.statusText} - ${errorText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error updating document with text:', error);
    throw error;
  }
}

/**
 * Update a document with file content
 * 
 * @param apiBaseUrl - Base URL for the API
 * @param documentId - ID of the document to update
 * @param file - File to update the document with
 * @param authToken - Authentication token
 * @param options - Optional parameters
 * @returns The updated document metadata
 */
export async function updateDocumentWithFile(
  apiBaseUrl: string,
  documentId: string,
  file: File,
  authToken: string | null,
  options?: {
    metadata?: Record<string, any>;
    rules?: Array<Record<string, any>>;
    updateStrategy?: string;
    useColpali?: boolean;
  }
): Promise<Document> {
  try {
    let url = `${apiBaseUrl}/documents/${documentId}/update_file`;
    const queryParams: string[] = [];
    
    if (options?.useColpali !== undefined) {
      queryParams.push(`use_colpali=${options.useColpali}`);
    }
    
    if (queryParams.length > 0) {
      url += `?${queryParams.join('&')}`;
    }

    const formData = new FormData();
    formData.append('file', file);
    
    if (options?.metadata) {
      formData.append('metadata', JSON.stringify(options.metadata));
    }
    
    if (options?.rules) {
      formData.append('rules', JSON.stringify(options.rules));
    }
    
    if (options?.updateStrategy) {
      formData.append('update_strategy', options.updateStrategy);
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: createAuthHeaders(authToken),
      body: formData
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to update document with file: ${response.statusText} - ${errorText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error updating document with file:', error);
    throw error;
  }
}

/**
 * Update a document's metadata
 * 
 * @param apiBaseUrl - Base URL for the API
 * @param documentId - ID of the document to update
 * @param metadata - New metadata to merge with existing metadata
 * @param authToken - Authentication token
 * @returns The updated document metadata
 */
export async function updateDocumentMetadata(
  apiBaseUrl: string,
  documentId: string,
  metadata: Record<string, any>,
  authToken: string | null
): Promise<Document> {
  try {
    const url = `${apiBaseUrl}/documents/${documentId}/update_metadata`;

    const response = await fetch(url, {
      method: 'POST',
      headers: createAuthHeaders(authToken, 'application/json'),
      body: JSON.stringify({ metadata })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to update document metadata: ${response.statusText} - ${errorText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error updating document metadata:', error);
    throw error;
  }
}
