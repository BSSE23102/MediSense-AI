import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, OCRResponse, SummaryResponse } from '../../services/api.service';
import { LoaderComponent } from '../../components/loader/loader.component';
import { TextSliderComponent } from '../../components/text-slider/text-slider.component';

@Component({
  selector: 'app-report',
  standalone: true,
  imports: [CommonModule, LoaderComponent, TextSliderComponent],
  templateUrl: './report.component.html',
  styleUrl: './report.component.css'
})
export class ReportComponent {
  selectedFile: File | null = null;
  isDragging = false;
  isProcessing = false;
  extractedText = '';
  summary: SummaryResponse | null = null;
  error = '';

  constructor(private apiService: ApiService) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.handleFile(file);
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
    
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  handleFile(file: File) {
    // Validate file type
    const validTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
      this.error = 'Please upload a PDF or image file (PNG, JPG, JPEG)';
      return;
    }

    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
      this.error = 'File size must be less than 16MB';
      return;
    }

    this.selectedFile = file;
    this.error = '';
    this.processFile();
  }

  processFile() {
    if (!this.selectedFile) return;

    this.isProcessing = true;
    this.error = '';
    this.summary = null;

    // Step 1: Extract text with OCR
    this.apiService.extractText(this.selectedFile).subscribe({
      next: (response) => {
        if (response.success) {
          this.extractedText = response.extracted_text;
          // Step 2: Summarize the extracted text
          this.summarizeText();
        } else {
          this.error = 'Failed to extract text from the file';
          this.isProcessing = false;
        }
      },
      error: (err) => {
        this.error = 'Error processing file. Please try again.';
        this.isProcessing = false;
        console.error('OCR Error:', err);
      }
    });
  }

  summarizeText() {
    if (!this.extractedText) return;

    this.apiService.summarizeReport(this.extractedText).subscribe({
      next: (response) => {
        if (response.success) {
          this.summary = response;
        } else {
          this.error = 'Failed to generate summary';
        }
        this.isProcessing = false;
      },
      error: (err) => {
        this.error = 'Error generating summary. Please try again.';
        this.isProcessing = false;
        console.error('Summary Error:', err);
      }
    });
  }

  reset() {
    this.selectedFile = null;
    this.extractedText = '';
    this.summary = null;
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
}
