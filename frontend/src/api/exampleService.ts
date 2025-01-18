import axiosInstance from "./axiosInstance";

export async function fetchData(path: string): Promise<{}> {
  try {
    const response = await axiosInstance.get(path);
    return response.data;
  } catch (error: any) {
    console.error("Error fetching data:", error);
    throw error;
  }
}
