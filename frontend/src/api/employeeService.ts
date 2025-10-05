import { Employee } from '../types/Employee';

const API_BASE_URL: string = process.env.NEXT_PUBLIC_API_URL || '/api';

class EmployeeService {
  async getAllEmployees(): Promise<Employee[]> {
    const response = await fetch(`${API_BASE_URL}/employees`);
    if (!response.ok) {
      throw new Error('Failed to fetch employees');
    }
    return response.json();
  }
}

export const employeeService = new EmployeeService();