import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, SymptomResponse } from '../../services/api.service';
import { LoaderComponent } from '../../components/loader/loader.component';
import { TextSliderComponent } from '../../components/text-slider/text-slider.component';

@Component({
  selector: 'app-symptoms',
  standalone: true,
  imports: [CommonModule, FormsModule, LoaderComponent, TextSliderComponent],
  templateUrl: './symptoms.component.html',
  styleUrl: './symptoms.component.css'
})
export class SymptomsComponent {
  symptoms = '';
  isAnalyzing = false;
  analysis: SymptomResponse | null = null;
  error = '';

  constructor(private apiService: ApiService) {}

  analyzeSymptoms() {
    if (!this.symptoms.trim()) {
      this.error = 'Please describe your symptoms';
      return;
    }

    this.isAnalyzing = true;
    this.error = '';
    this.analysis = null;

    this.apiService.checkSymptoms(this.symptoms).subscribe({
      next: (response) => {
        if (response.success) {
          this.analysis = response;
        } else {
          this.error = 'Failed to analyze symptoms';
        }
        this.isAnalyzing = false;
      },
      error: (err) => {
        this.error = 'Error analyzing symptoms. Please try again.';
        this.isAnalyzing = false;
        console.error('Symptom Analysis Error:', err);
      }
    });
  }

  reset() {
    this.symptoms = '';
    this.analysis = null;
    this.error = '';
  }

  getUrgencyClass(urgency: string): string {
    switch (urgency?.toLowerCase()) {
      case 'high': return 'badge-danger';
      case 'medium': return 'badge-warning';
      case 'low': return 'badge-success';
      default: return 'badge-info';
    }
  }

  getProbabilityClass(probability: string): string {
    switch (probability?.toLowerCase()) {
      case 'high': return 'probability-high';
      case 'medium': return 'probability-medium';
      case 'low': return 'probability-low';
      default: return '';
    }
  }
}
