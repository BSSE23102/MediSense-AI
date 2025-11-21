import { Component, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { TextSliderComponent } from '../../components/text-slider/text-slider.component';

declare var Chart: any;

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink, TextSliderComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements AfterViewInit {
  @ViewChild('diseaseChart') diseaseChart!: ElementRef<HTMLCanvasElement>;
  @ViewChild('accessChart') accessChart!: ElementRef<HTMLCanvasElement>;
  @ViewChild('accuracyChart') accuracyChart!: ElementRef<HTMLCanvasElement>;
  features = [
    {
      icon: 'file-text',
      title: 'Report Analysis',
      description: 'Upload medical reports and get AI-powered summaries in both patient-friendly and technical formats'
    },
    {
      icon: 'heartbeat',
      title: 'Symptom Checker',
      description: 'Describe your symptoms and receive evidence-based analysis with risk assessment'
    },
    {
      icon: 'shield-check',
      title: 'Secure & Private',
      description: 'Your health data is processed securely with enterprise-grade encryption'
    }
  ];

  stats = [
    { value: '10K+', label: 'Reports Analyzed' },
    { value: '98%', label: 'Accuracy Rate' },
    { value: '24/7', label: 'Availability' }
  ];

  ngAfterViewInit() {
    this.initCharts();
  }

  initCharts() {
    // Disease Prevalence Chart
    new Chart(this.diseaseChart.nativeElement, {
      type: 'bar',
      data: {
        labels: ['Diabetes', 'Hypertension', 'Heart Disease', 'Cancer', 'Respiratory'],
        datasets: [{
          label: 'Cases per 100k',
          data: [10500, 31400, 6950, 4420, 8100],
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
          borderColor: 'rgba(255, 255, 255, 0.3)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(17, 17, 17, 0.95)',
            titleColor: '#ffffff',
            bodyColor: '#a0a0a0',
            borderColor: '#222222',
            borderWidth: 1
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#a0a0a0' }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#a0a0a0' }
          }
        }
      }
    });

    // Healthcare Accessibility Chart
    new Chart(this.accessChart.nativeElement, {
      type: 'doughnut',
      data: {
        labels: ['Urban Access', 'Rural Access', 'Limited Access', 'No Access'],
        datasets: [{
          data: [45, 30, 18, 7],
          backgroundColor: [
            'rgba(255, 255, 255, 0.15)',
            'rgba(255, 255, 255, 0.1)',
            'rgba(255, 255, 255, 0.06)',
            'rgba(255, 255, 255, 0.03)'
          ],
          borderColor: '#222222',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#a0a0a0', padding: 15 }
          },
          tooltip: {
            backgroundColor: 'rgba(17, 17, 17, 0.95)',
            titleColor: '#ffffff',
            bodyColor: '#a0a0a0',
            borderColor: '#222222',
            borderWidth: 1
          }
        }
      }
    });

    // AI Accuracy Chart
    new Chart(this.accuracyChart.nativeElement, {
      type: 'line',
      data: {
        labels: ['2020', '2021', '2022', '2023', '2024'],
        datasets: [{
          label: 'Accuracy %',
          data: [87, 91, 94, 96, 98],
          borderColor: 'rgba(255, 255, 255, 0.5)',
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(17, 17, 17, 0.95)',
            titleColor: '#ffffff',
            bodyColor: '#a0a0a0',
            borderColor: '#222222',
            borderWidth: 1
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            min: 80,
            max: 100,
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#a0a0a0' }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#a0a0a0' }
          }
        }
      }
    });
  }
}
