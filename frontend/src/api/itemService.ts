import axiosInstance from "./axiosInstance";

export async function createItem(payload: {
  name: string;
  description: string;
  price: number;
  is_available: boolean;
}): Promise<{}> {
  const path = "/items/";
  try {
    const response = await axiosInstance.post(path, payload);
    return response.data;
  } catch (error: any) {
    console.error("Error creating item:", error);
    throw error;
  }
}
