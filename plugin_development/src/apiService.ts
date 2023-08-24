import axios, { AxiosRequestConfig } from 'axios';
import FormData = require("form-data");

export async function sendAPIRequest<T>(
  url: string,
  method: string,
  data?: T,
  formData?: FormData,
  params?: any,
  headers?: any,
  contentType?: string
): Promise<any> {
  const config: AxiosRequestConfig = {
    url,
    method,
    data,
    params,
    headers,
  };

  if (formData) {
    config.headers = {
      ...config.headers,
      'Content-Type': contentType,
    };
    config.data = formData;
  }

  try {
    const response = await axios(config);
    return response;
  } catch (error: any) {
    throw new Error(error.response?.data?.message || error.message);
  }
}