'use client';

import React, { useState, useEffect } from 'react';
import PageTemplate from '@/components/PageTemplate';
import { employeeService } from '@/api/employeeService';
import { Employee } from '@/types/Employee';
import { Phone } from 'lucide-react';

const VoiceSimulationsPage: React.FC = () => {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const handleCreateCall = async (employee: Employee) => {
    console.log('Creating call for employee:', employee);
    
    try {
      // Call the simulate-call API endpoint
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/simulate-call`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          employee_id: employee.id,
          phone_number: employee.phone_number,
          scenario_type: 'default'
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to initiate call: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('Call simulation response:', result);
      
      // Show success message
      alert(`Call simulation initiated successfully!\n\nCall ID: ${result.call_id}\nEmployee: ${result.employee_name}\nPhone: ${result.employee_phone}\n\nStatus: ${result.message}`);
      
    } catch (error) {
      console.error('Error initiating call:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      alert(`Failed to initiate call for ${employee.name}. Please try again.\n\nError: ${errorMessage}`);
    }
  };

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const data = await employeeService.getAllEmployees();
        setEmployees(data);
      } catch (err) {
        setError('Failed to fetch employees');
        console.error('Error fetching employees:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchEmployees();
  }, []);

  return (
    <PageTemplate title="Voice Simulations" description="Employee information display">
      <div className="container mx-auto p-6">        
        {loading && <p className="text-[var(--color-text-muted)]">Loading employees...</p>}
        {error && <p className="text-red-400">{error}</p>}
        
        {!loading && !error && (
          <div className="overflow-x-auto rounded-lg border border-[var(--color-border)]">
            <table className="min-w-full bg-[var(--color-surface)] text-white table-fixed">
              <colgroup>
                <col className="w-24" />
                <col className="w-80" />
                <col className="w-48" />
                <col className="w-32" />
              </colgroup>
              <thead>
                <tr className="bg-[var(--color-sidebar-background)] border-b border-[var(--color-border)]">
                  <th className="pl-4 pr-4 px-8 py-5 font-semibold text-white resize-x overflow-hidden">
                    <div className="pl-4 pr-4">ID</div>
                  </th>
                  <th className="pl-4 pr-4 px-8 py-5 font-semibold text-white resize-x overflow-hidden">
                    <div className="pl-4 pr-4">Name</div>
                  </th>
                  <th className="pl-4 pr-4 px-8 py-5 font-semibold text-white resize-x overflow-hidden">
                    <div className="pl-4 pr-4">Phone Number</div>
                  </th>
                  <th className="pl-4 pr-4 px-8 py-5 font-semibold text-white resize-x overflow-hidden">
                    <div className="pl-4 pr-4">Actions</div>
                  </th>
                </tr>
              </thead>
              <tbody>
                {employees.map((employee) => (
                  <tr key={employee.id} className="border-b border-[var(--color-border)] hover:bg-[var(--color-sidebar-hover)] transition-colors duration-150">
                    <td className="text-center paddingClass px-8 py-5 text-[var(--color-foreground)] truncate">{employee.id}</td>
                    <td className="text-center paddingClass px-8 py-5 text-[var(--color-foreground)] truncate">{employee.name}</td>
                    <td className="text-center paddingClass px-8 py-5 text-[var(--color-text-muted)] truncate">{employee.phone_number}</td>
                    <td className="text-center paddingClass px-8 py-5">
                      <button
                        onClick={() => handleCreateCall(employee)}
                        className="bg-[var(--color-accent)] hover:bg-blue-600 text-white p-3 rounded-lg transition-colors duration-150"
                        title={`Call ${employee.name}`}
                      >
                        <Phone size={20} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </PageTemplate>
  );
};

export default VoiceSimulationsPage;