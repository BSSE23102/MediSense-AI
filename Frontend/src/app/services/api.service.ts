import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface OCRResponse {
  success: boolean;
  extracted_text: string;
  confidence: number;
}

export interface SummaryResponse {
  success: boolean;
  patient_summary: string;
  doctor_summary: string;
  key_findings: string[];
  medications?: string[];
  critical_warnings?: string[];
  follow_up?: string;
}

export interface SymptomResponse {
  success: boolean;
  possible_conditions: Array<{
    name: string;
    probability: string;
    description: string;
  }>;
  urgency: string;
  explanation: string;
  recommendations: string[];
  citations?: string[];
  seek_immediate_care_if?: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  // OCR Text Extraction
  extractText(file: File): Observable<OCRResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<OCRResponse>(`${this.apiUrl}/ocr`, formData);
  }

  // Report Summarization
  summarizeReport(text: string): Observable<SummaryResponse> {
    return this.http.post<SummaryResponse>(`${this.apiUrl}/summarize`, { text });
  }

  // Symptom Analysis
  checkSymptoms(symptoms: string): Observable<SymptomResponse> {
    return this.http.post<SymptomResponse>(`${this.apiUrl}/symptom-check`, { symptoms });
  }
}
