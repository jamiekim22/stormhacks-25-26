export interface Employee {
  id: number;
  name: string;
  phone_number: string;
  company?: string;
}

export interface CallSimulationRequest {
  employee_id: number;
  scenario_type: string;
}

export interface CallSimulationResponse {
  call_id: string;
  status: string;
  message: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}