'use client';

import React, { useState, useEffect } from 'react';
import PageTemplate from '@/components/PageTemplate';
import { employeeService } from '@/api/employeeService';
import { Employee } from '@/types/Employee';
import { SecurityAssessment } from '@/types/SecurityAssessment';
import { ChevronDown, User, Calendar, Shield, AlertTriangle } from 'lucide-react';

const EmployeesPage: React.FC = () => {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [assessments, setAssessments] = useState<SecurityAssessment[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingAssessments, setLoadingAssessments] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dropdownOpen, setDropdownOpen] = useState(false);

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

  const handleEmployeeSelect = async (employee: Employee) => {
    setSelectedEmployee(employee);
    setDropdownOpen(false);
    setLoadingAssessments(true);
    setError(null);

    try {
      const assessmentData = await employeeService.getSecurityAssessments(employee.id);
      setAssessments(assessmentData);
    } catch (err) {
      setError(`Failed to fetch security assessments for ${employee.name}`);
      console.error('Error fetching assessments:', err);
      setAssessments([]);
    } finally {
      setLoadingAssessments(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'Low': return 'text-green-400 bg-green-400/10';
      case 'Medium': return 'text-yellow-400 bg-yellow-400/10';
      case 'High': return 'text-red-400 bg-red-400/10';
      default: return 'text-gray-400 bg-gray-400/10';
    }
  };

  return (
    <PageTemplate
      title="Employee Security Assessments"
      description="View security assessment history for individual employees"
    >
      <div className="container mx-auto p-6">
        {loading && <p className="text-[var(--color-text-muted)]">Loading employees...</p>}
        {error && <p className="text-red-400 mb-4">{error}</p>}

        {!loading && (
          <>
            {/* Employee Dropdown */}
            <div className="mb-8">
              <label className="block text-sm font-medium text-white mb-2">
                Select Employee
              </label>
              <div className="relative">
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="w-full max-w-md bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg px-4 py-3 text-left text-white hover:bg-[var(--color-sidebar-hover)] transition-colors duration-150 flex items-center justify-between"
                >
                  <div className="flex items-center">
                    <User size={16} className="mr-2 text-[var(--color-text-muted)]" />
                    <span>
                      {selectedEmployee ? selectedEmployee.name : 'Choose an employee...'}
                    </span>
                  </div>
                  <ChevronDown 
                    size={16} 
                    className={`text-[var(--color-text-muted)] transition-transform duration-150 ${
                      dropdownOpen ? 'transform rotate-180' : ''
                    }`} 
                  />
                </button>

                {dropdownOpen && (
                  <div className="absolute z-10 w-full max-w-md mt-1 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    {employees.map((employee) => (
                      <button
                        key={employee.id}
                        onClick={() => handleEmployeeSelect(employee)}
                        className="w-full px-4 py-3 text-left text-white hover:bg-[var(--color-sidebar-hover)] transition-colors duration-150 flex items-center"
                      >
                        <User size={14} className="mr-2 text-[var(--color-text-muted)]" />
                        <div>
                          <div className="font-medium">{employee.name}</div>
                          <div className="text-sm text-[var(--color-text-muted)]">{employee.phone_number}</div>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Security Assessments Table */}
            {selectedEmployee && (
              <div>
                <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                  <Shield size={20} className="mr-2 text-[var(--color-accent)]" />
                  Security Assessments for {selectedEmployee.name}
                </h3>

                {loadingAssessments && (
                  <p className="text-[var(--color-text-muted)]">Loading assessments...</p>
                )}

                {!loadingAssessments && assessments.length === 0 && (
                  <div className="text-center py-8">
                    <AlertTriangle size={48} className="mx-auto text-[var(--color-text-muted)] mb-4" />
                    <p className="text-[var(--color-text-muted)]">No security assessments found for this employee.</p>
                  </div>
                )}

                {!loadingAssessments && assessments.length > 0 && (
                  <div className="overflow-x-auto rounded-lg border border-[var(--color-border)]">
                    <table className="min-w-full bg-[var(--color-surface)] text-white">
                      <thead>
                        <tr className="bg-[var(--color-sidebar-background)] border-b border-[var(--color-border)]">
                          <th className="px-6 py-4 text-left font-semibold text-white">
                            <Calendar size={16} className="inline mr-2" />
                            Date
                          </th>
                          <th className="px-6 py-4 text-left font-semibold text-white">Score</th>
                          <th className="px-6 py-4 text-left font-semibold text-white">Resistance Level</th>
                          <th className="px-6 py-4 text-left font-semibold text-white">SE Susceptibility</th>
                          <th className="px-6 py-4 text-left font-semibold text-white">Feedback</th>
                        </tr>
                      </thead>
                      <tbody>
                        {assessments.map((assessment) => (
                          <tr key={assessment.id} className="border-b border-[var(--color-border)] hover:bg-[var(--color-sidebar-hover)] transition-colors duration-150">
                            <td className="px-6 py-4 text-[var(--color-foreground)]">
                              {new Date(assessment.assessment_date).toLocaleDateString()} {new Date(assessment.assessment_date).toLocaleTimeString()}
                            </td>
                            <td className={`px-6 py-4 font-semibold ${getScoreColor(assessment.security_score)}`}>
                              {assessment.security_score}%
                            </td>
                            <td className="px-6 py-4">
                              <span className={`px-3 py-1 rounded-full text-xs font-medium ${getLevelColor(assessment.resistance_level)}`}>
                                {assessment.resistance_level}
                              </span>
                            </td>
                            <td className="px-6 py-4">
                              <span className={`px-3 py-1 rounded-full text-xs font-medium ${getLevelColor(assessment.social_engineering_susceptibility)}`}>
                                {assessment.social_engineering_susceptibility}
                              </span>
                            </td>
                            <td className="px-6 py-4 text-[var(--color-text-muted)] max-w-xs truncate">
                              {assessment.feedback || 'No feedback provided'}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </PageTemplate>
  );
};

export default EmployeesPage;
