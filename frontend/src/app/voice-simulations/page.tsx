'use client';

import React, { useState, useEffect } from 'react';
import PageTemplate from '@/components/PageTemplate';
import { employeeService } from '@/api/employeeService';
import { Employee } from '@/types/Employee';

const VoiceSimulationsPage: React.FC = () => {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
                </tr>
              </thead>
              <tbody>
                {employees.map((employee) => (
                  <tr key={employee.id} className="border-b border-[var(--color-border)] hover:bg-[var(--color-sidebar-hover)] transition-colors duration-150">
                    <td className="text-center paddingClass px-8 py-5 text-[var(--color-foreground)] truncate">{employee.id}</td>
                    <td className="text-center paddingClass px-8 py-5 text-[var(--color-foreground)] truncate">{employee.name}</td>
                    <td className="text-center paddingClass px-8 py-5 text-[var(--color-text-muted)] truncate">{employee.phone_number}</td>
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