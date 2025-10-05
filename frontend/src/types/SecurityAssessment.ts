export interface SecurityAssessment {
  id: number;
  employee_id: number;
  assessment_date: string;
  security_score: number;
  resistance_level: 'Low' | 'Medium' | 'High';
  social_engineering_susceptibility: 'Low' | 'Medium' | 'High';
  feedback?: string;
  scoring_explanation?: string;
}