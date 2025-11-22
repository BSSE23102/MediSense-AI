import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ReportComponent } from './pages/report/report.component';
import { SymptomsComponent } from './pages/symptoms/symptoms.component';
import { AboutComponent } from './pages/about/about.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'report', component: ReportComponent },
  { path: 'symptoms', component: SymptomsComponent },
  { path: 'about', component: AboutComponent },
  { path: '**', redirectTo: '' }
];
