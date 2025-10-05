'use client';

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Search, Phone, User, Building2 } from 'lucide-react';
import { Employee } from '../../types/Employee';
import { employeeService } from '../../api/employeeService';
import PageTemplate from '../../components/PageTemplate';
import './VoiceSimulationsPage.css';

interface VoiceSimulationsPageProps {
  className?: string;
}

const VoiceSimulationsPage: React.FC<VoiceSimulationsPageProps> = ({ className }) => {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [isSearchFocused, setIsSearchFocused] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [callInProgress, setCallInProgress] = useState<boolean>(false);

  // Fetch employees from Snowflake API
  useEffect(() => {
    const fetchEmployees = async (): Promise<void> => {
      try {
        setLoading(true);
        setError(null);
        const data = await employeeService.getAllEmployees();
        setEmployees(data);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchEmployees();
  }, []);

  // Filter employees based on search term
  const filteredEmployees = useMemo<Employee[]>(() => {
    if (!searchTerm.trim()) return employees;
    
    const searchLower = searchTerm.toLowerCase();
    return employees.filter(employee =>
      employee.name.toLowerCase().includes(searchLower) ||
      employee.phone_number.includes(searchTerm) ||
      (employee.company && employee.company.toLowerCase().includes(searchLower))
    );
  }, [employees, searchTerm]);

  // Get top 5 results for dropdown
  const dropdownResults = useMemo<Employee[]>(() => {
    return filteredEmployees.slice(0, 5);
  }, [filteredEmployees]);

  const handleSearchChange = useCallback((e: React.ChangeEvent<HTMLInputElement>): void => {
    setSearchTerm(e.target.value);
  }, []);

  const handleEmployeeSelect = useCallback((employee: Employee): void => {
    setSelectedEmployee(employee);
    setSearchTerm(employee.name);
    setIsSearchFocused(false);
  }, []);

  const handleCallSimulation = useCallback(async (employee: Employee): Promise<void> => {
    if (callInProgress) return;

    try {
      setCallInProgress(true);
      const response = await employeeService.simulateCall(employee.id, 'default');
      
      if (response.status === 'success') {
        alert(`Call simulation initiated for ${employee.name}`);
      } else {
        throw new Error(response.message || 'Failed to initiate call');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      alert(`Error: ${errorMessage}`);
    } finally {
      setCallInProgress(false);
    }
  }, [callInProgress]);

  const formatPhoneNumber = useCallback((phone: string): string => {
    if (!phone) return 'N/A';
    const cleaned = phone.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
      return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phone;
  }, []);

  const handleSearchFocus = useCallback((): void => {
    setIsSearchFocused(true);
  }, []);

  const handleSearchBlur = useCallback((): void => {
    setTimeout(() => setIsSearchFocused(false), 200);
  }, []);

  return (
    <PageTemplate
      title="Voice Simulations"
      description="Select an employee to simulate a scam call"
      bodyClassName={className}
    >
      {loading && (
        <div className="loading-container">
          <div className="loading-spinner" />
          <p>Loading employees...</p>
        </div>
      )}

      {error && (
        <div className="error-container">
          <p>Error loading employees: {error}</p>
          <button onClick={() => window.location.reload()}>Retry</button>
        </div>
      )}

      {!loading && !error && (
        <div className="voice-simulations-content">

      {/* Search Bar Section */}
      <div className="search-section">
        <div className="search-container">
          <div className="search-input-wrapper">
            <Search className="search-icon" size={20} />
            <input
              type="text"
              placeholder="Search employees by name, phone, or company..."
              value={searchTerm}
              onChange={handleSearchChange}
              onFocus={handleSearchFocus}
              onBlur={handleSearchBlur}
              className="search-input"
            />
            
            {/* Search Dropdown */}
            {isSearchFocused && searchTerm && dropdownResults.length > 0 && (
              <div className="search-dropdown">
                {dropdownResults.map((employee) => (
                  <div
                    key={employee.id}
                    className="dropdown-item"
                    onClick={() => handleEmployeeSelect(employee)}
                    role="button"
                    tabIndex={0}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        handleEmployeeSelect(employee);
                      }
                    }}
                  >
                    <div className="dropdown-item-avatar">
                      <User size={16} />
                    </div>
                    <div className="dropdown-item-info">
                      <span className="dropdown-item-name">{employee.name}</span>
                      <span className="dropdown-item-details">
                        {employee.company || 'Company'} • {formatPhoneNumber(employee.phone_number)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <button 
            className="call-button"
            onClick={() => selectedEmployee && handleCallSimulation(selectedEmployee)}
            disabled={!selectedEmployee || callInProgress}
            type="button"
          >
            <Phone size={18} />
            {callInProgress ? 'Calling...' : 'Call'}
          </button>
        </div>
      </div>

      {/* Employee Table */}
      <div className="table-section">
        <div className="table-header">
          <h2>All Employees ({filteredEmployees.length})</h2>
        </div>
        
        <div className="table-container">
          <table className="employees-table">
            <thead>
              <tr>
                <th>Employee</th>
                <th>Company</th>
                <th>Phone Number</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredEmployees.map((employee) => (
                <tr key={employee.id}>
                  <td>
                    <div className="employee-info">
                      <div className="employee-avatar">
                        <User size={20} />
                      </div>
                      <span className="employee-name">{employee.name}</span>
                    </div>
                  </td>
                  <td>
                    <div className="company-info">
                      <Building2 size={16} />
                      <span>{employee.company || 'Company Name'}</span>
                    </div>
                  </td>
                  <td className="phone-number">
                    {formatPhoneNumber(employee.phone_number)}
                  </td>
                  <td>
                    <button
                      className="table-call-button"
                      onClick={() => handleCallSimulation(employee)}
                      disabled={callInProgress}
                      type="button"
                    >
                      <Phone size={16} />
                      {callInProgress ? 'Calling...' : 'Call'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {filteredEmployees.length === 0 && (
            <div className="no-results">
              <p>No employees found matching your search.</p>
            </div>
          )}
        </div>
      </div>
        </div>
      )}
    </PageTemplate>
  );
};

export default VoiceSimulationsPage;