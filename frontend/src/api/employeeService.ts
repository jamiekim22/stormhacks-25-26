import { Employee } from '../types/Employee';
import { SecurityAssessment } from '../types/SecurityAssessment';

const API_BASE_URL: string = process.env.NEXT_PUBLIC_API_URL || '/api';

class EmployeeService {
  async getAllEmployees(): Promise<Employee[]> {
    const response = await fetch(`${API_BASE_URL}/employees`);
    if (!response.ok) {
      throw new Error('Failed to fetch employees');
    }
    return response.json();
  }

  async getSecurityAssessments(employeeId: number): Promise<SecurityAssessment[]> {
    const response = await fetch(`${API_BASE_URL}/employees/${employeeId}/security-assessments`);
    if (!response.ok) {
      throw new Error(`Failed to fetch security assessments for employee ${employeeId}`);
    }
    return response.json();
  }
}

export const employeeService = new EmployeeService();