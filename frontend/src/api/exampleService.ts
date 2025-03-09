import axiosInstance from "./axiosInstance";

export async function fetchData(): Promise<{}> {
  const path = "/";
  try {
    const response = await axiosInstance.get(path);
    return response.data;
  } catch (error: any) {
    console.error("Error fetching data:", error);
    throw error;
  }
}
