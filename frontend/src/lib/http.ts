// Simple fetch wrapper to avoid axios weirdness with URL resolution
export const http = {
  get: async (url: string) => {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: response.statusText }));
      const error: any = new Error(errorData.detail || 'Request failed');
      error.response = { data: errorData };
      throw error;
    }
    
    return { data: await response.json() };
  },
  
  post: async (url: string, data?: any) => {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: response.statusText }));
      const error: any = new Error(errorData.detail || 'Request failed');
      error.response = { data: errorData };
      throw error;
    }
    
    return { data: await response.json() };
  },
};