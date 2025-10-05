import { Employee, CallSimulationRequest, CallSimulationResponse } from '../types/Employee';

const API_BASE_URL: string = process.env.NEXT_PUBLIC_API_URL || '/api';

class EmployeeService {
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Network error' }));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async getAllEmployees(): Promise<Employee[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/employees`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return this.handleResponse<Employee[]>(response);
    } catch (error) {
      console.error('Error fetching employees:', error);
      throw new Error('Failed to fetch employees');
    }
  }

  async getEmployee(employeeId: number): Promise<Employee> {
    try {
      const response = await fetch(`${API_BASE_URL}/employees/${employeeId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return this.handleResponse<Employee>(response);
    } catch (error) {
      console.error(`Error fetching employee ${employeeId}:`, error);
      throw new Error('Failed to fetch employee');
    }
  }

  async simulateCall(
    employeeId: number, 
    scenarioType: string = 'default'
  ): Promise<CallSimulationResponse> {
    try {
      const requestBody: CallSimulationRequest = {
        employee_id: employeeId,
        scenario_type: scenarioType,
      };

      const response = await fetch(`${API_BASE_URL}/simulate-call`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });
      
      return this.handleResponse<CallSimulationResponse>(response);
    } catch (error) {
      console.error('Error simulating call:', error);
      throw new Error('Failed to initiate call simulation');
    }
  }

  async getCallStatus(callId: string): Promise<{ status: string; details?: any }> {
    try {
      const response = await fetch(`${API_BASE_URL}/call-status/${callId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return this.handleResponse<{ status: string; details?: any }>(response);
    } catch (error) {
      console.error(`Error fetching call status ${callId}:`, error);
      throw new Error('Failed to fetch call status');
    }
  }
}

export const employeeService = new EmployeeService();